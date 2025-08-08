import os
import re
import io
import base64
import json
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns
from app.llm_client import call_openai

sns.set(style="whitegrid")

def _encode_image_to_datauri(fig, fmt="png", max_bytes=100000):
    buf = io.BytesIO()
    fig.savefig(buf, format=fmt, bbox_inches="tight", dpi=100)
    buf.seek(0)
    data = buf.read()
    if len(data) > max_bytes and fmt != "webp":
        buf = io.BytesIO()
        fig.savefig(buf, format="webp", optimize=True, quality=60)
        buf.seek(0)
        data = buf.read()
        fmt = "webp"
    encoded = base64.b64encode(data).decode("ascii")
    return f"data:image/{fmt};base64,{encoded}", len(data)

def scrape_wikipedia_table(url: str) -> pd.DataFrame:
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table", {"class": lambda v: v and "wikitable" in v})
    if table is None:
        table = soup.find("table")
    df = pd.read_html(str(table))[0]
    return df

def try_parse_dates(df: pd.DataFrame):
    for col in df.columns:
        if df[col].dtype == object:
            try:
                df[col] = pd.to_datetime(df[col], errors='ignore')
            except Exception:
                pass
    return df

def parse_questions_text(q_text: str) -> dict:
    result = {"raw": q_text}
    urls = re.findall(r"https?://\S+", q_text)
    result['urls'] = urls
    if 'JSON array' in q_text or 'JSON array of strings' in q_text:
        result['format'] = 'json_array'
    elif 'JSON object' in q_text or ('{' in q_text and '}' in q_text):
        result['format'] = 'json_object'
    else:
        result['format'] = 'json'
    return result

def process_request(q_text: str, saved_files: dict, tmpdir: str):
    parsed = parse_questions_text(q_text)

    # Wikipedia scrape case
    if parsed['urls']:
        url = parsed['urls'][0]
        df = scrape_wikipedia_table(url)
        df = try_parse_dates(df)
        answers = []
        lines = [l.strip() for l in q_text.splitlines() if l.strip()]
        for line in lines:
            if re.match(r"^\d+\.", line):
                q = line
                if 'How many' in q and '$2 bn' in q:
                    col = next((c for c in df.columns if 'Gross' in c or 'Worldwide' in c or 'gross' in c.lower()), None)
                    if col:
                        vals = df[col].astype(str).str.replace(r"[^0-9\.]+", "", regex=True)
                        vals = pd.to_numeric(vals, errors='coerce')
                        count = int((vals >= 2000000000).sum())
                        answers.append(count)
                    continue
                if 'Which is the earliest film' in q:
                    year_col = next((c for c in df.columns if 'Year' in c or 'Release' in c), None)
                    name_col = next((c for c in df.columns if 'Title' in c or 'Film' in c or 'Name' in c), df.columns[0])
                    money_col = next((c for c in df.columns if 'Gross' in c or 'Worldwide' in c or 'Peak' in c), None)
                    if money_col and year_col:
                        df[money_col] = df[money_col].astype(str).str.replace(r"[^0-9\.]+", "", regex=True)
                        df[money_col] = pd.to_numeric(df[money_col], errors='coerce')
                        mask = df[money_col] > 1500000000
                        if mask.any():
                            earliest = df.loc[mask].sort_values(year_col).iloc[0][name_col]
                            answers.append(str(earliest))
                    continue
                if 'correlation' in q.lower() and 'Rank' in q and 'Peak' in q:
                    if 'Rank' in df.columns and 'Peak' in df.columns:
                        x = pd.to_numeric(df['Rank'], errors='coerce')
                        y = pd.to_numeric(df['Peak'].astype(str).str.replace(r"[^0-9\.]+", "", regex=True), errors='coerce')
                        corr = float(x.corr(y))
                        answers.append(round(corr, 6))
                    continue
                if 'scatterplot' in q.lower() and 'Rank' in q and 'Peak' in q:
                    fig, ax = plt.subplots(figsize=(6,4))
                    x = pd.to_numeric(df['Rank'], errors='coerce')
                    y = pd.to_numeric(df['Peak'].astype(str).str.replace(r"[^0-9\.]+", "", regex=True), errors='coerce')
                    ax.scatter(x, y, s=30)
                    ax.set_xlabel('Rank')
                    ax.set_ylabel('Peak')
                    mask = x.notna() & y.notna()
                    if mask.sum() >= 2:
                        slope, intercept = np.polyfit(x[mask], y[mask], 1)
                        xs = np.linspace(x[mask].min(), x[mask].max(), 100)
                        ys = slope * xs + intercept
                        ax.plot(xs, ys, linestyle=':', color='red')
                    datauri, _ = _encode_image_to_datauri(fig, fmt='png', max_bytes=100000)
                    plt.close(fig)
                    answers.append(datauri)
                    continue
        return answers

    # CSV case
    csv_path = None
    for name, path in saved_files.items():
        if name.lower().endswith('.csv'):
            csv_path = path
            break
    if csv_path:
        df = pd.read_csv(csv_path)
        parsed_lines = [l.strip() for l in q_text.splitlines() if l.strip()]
        if any('scatterplot' in l.lower() for l in parsed_lines):
            num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            xcol = num_cols[0] if len(num_cols) > 0 else df.columns[0]
            ycol = num_cols[1] if len(num_cols) > 1 else num_cols[0]
            fig, ax = plt.subplots(figsize=(6,4))
            ax.scatter(df[xcol], df[ycol], s=20)
            ax.set_xlabel(xcol)
            ax.set_ylabel(ycol)
            mask = df[xcol].notna() & df[ycol].notna()
            if mask.sum() >= 2:
                slope, intercept = np.polyfit(df.loc[mask, xcol], df.loc[mask, ycol], 1)
                xs = np.linspace(df.loc[mask, xcol].min(), df.loc[mask, xcol].max(), 100)
                ys = slope * xs + intercept
                ax.plot(xs, ys, linestyle=':', color='red')
            datauri, _ = _encode_image_to_datauri(fig, fmt='png', max_bytes=100000)
            plt.close(fig)
            return {
                "columns": df.columns.tolist(),
                "preview": df.head(5).to_dict(orient='records'),
                "plot": datauri
            }
        return {"columns": df.columns.tolist(), "rows": min(50, len(df))}

    # Fallback to LLM
    plan = call_openai(q_text)
    if plan:
        return {"plan": plan}

    raise ValueError('Unable to handle request. Provide a Wikipedia URL or a CSV, or enable OPENAI_API_KEY for LLM parsing.')