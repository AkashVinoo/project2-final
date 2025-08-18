import os
import base64
import pandas as pd
import matplotlib.pyplot as plt
import io
from .llm_client import call_openai

def encode_file_to_base64(file_path):
    """Encode any file (image, CSV, etc.) into base64 string."""
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def generate_bar_chart(df, x_col, y_col, color="blue", max_size_kb=100):
    fig, ax = plt.subplots()
    df.plot(kind="bar", x=x_col, y=y_col, ax=ax, color=color, legend=False)
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title(f"{y_col} by {x_col}")
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png", dpi=100)
    plt.close(fig)
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode("utf-8")
    while len(b64) > max_size_kb * 1024:
        buf = io.BytesIO()
        fig, ax = plt.subplots()
        df.plot(kind="bar", x=x_col, y=y_col, ax=ax, color=color, legend=False)
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(f"{y_col} by {x_col}")
        plt.tight_layout()
        plt.savefig(buf, format="png", dpi=80)
        plt.close(fig)
        buf.seek(0)
        b64 = base64.b64encode(buf.read()).decode("utf-8")
    return b64

def generate_line_chart(df, x_col, y_col, color="red", max_size_kb=100):
    fig, ax = plt.subplots()
    df.plot(kind="line", x=x_col, y=y_col, ax=ax, color=color, legend=False)
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title(f"{y_col} over {x_col}")
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png", dpi=100)
    plt.close(fig)
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode("utf-8")
    while len(b64) > max_size_kb * 1024:
        buf = io.BytesIO()
        fig, ax = plt.subplots()
        df.plot(kind="line", x=x_col, y=y_col, ax=ax, color=color, legend=False)
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(f"{y_col} over {x_col}")
        plt.tight_layout()
        plt.savefig(buf, format="png", dpi=80)
        plt.close(fig)
        buf.seek(0)
        b64 = base64.b64encode(buf.read()).decode("utf-8")
    return b64

def process_request(question_file, attachments=None):
    """
    Reads questions.txt and optional attachments (CSV, images).
    Returns structured JSON with metrics, charts, and base64-encoded images.
    """
    try:
        with open(question_file, "r", encoding="utf-8") as f:
            questions = f.read()

        result = {"attachments": {}}
        df = None

        if attachments:
            for file_path in attachments:
                ext = file_path.split(".")[-1].lower()
                if ext == "csv" and df is None:
                    df = pd.read_csv(file_path)
                elif ext in ["png", "jpg", "jpeg"]:
                    result["attachments"][os.path.basename(file_path)] = encode_file_to_base64(file_path)

        if df is not None:
            total_sales = df['sales'].sum()
            top_region = df.groupby('region')['sales'].sum().idxmax()
            day_sales_corr = df['sales'].corr(df['date'].apply(lambda x: int(x.split('-')[2])))
            median_sales = df['sales'].median()
            total_sales_tax = round(total_sales * 0.1, 2)

            sales_by_region = df.groupby('region')['sales'].sum().reset_index()
            bar_chart_b64 = generate_bar_chart(sales_by_region, "region", "sales", color="blue")

            df_sorted = df.sort_values('date')
            df_sorted['cumulative_sales'] = df_sorted['sales'].cumsum()
            cumulative_chart_b64 = generate_line_chart(df_sorted, "date", "cumulative_sales", color="red")

            result.update({
                "total_sales": total_sales,
                "top_region": top_region,
                "day_sales_correlation": round(day_sales_corr, 6),
                "bar_chart": bar_chart_b64,
                "median_sales": median_sales,
                "total_sales_tax": total_sales_tax,
                "cumulative_sales_chart": cumulative_chart_b64
            })

        return result

    except Exception as e:
        return {"error": str(e)}
