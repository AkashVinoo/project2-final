# Data Analyst Agent

## Overview
The **Data Analyst Agent** is an API service that uses Large Language Models (LLMs) to source, prepare, analyze, and visualize data.  
It accepts analysis tasks and optional data files via a POST request and returns structured answers in the requested format (JSON, arrays, plots as Base64 images, etc.).

## API Specification

**Endpoint:**  
POST https://app.example.com/api/

**Request:**  
Multipart form-data with:
- questions.txt (mandatory): Text file containing task description/questions.
- Optional files: .csv, .json, .png, .pdf, .parquet, etc.

**Example:**
curl "https://app.example.com/api/" 
  -F "questions.txt=@question.txt" 
  -F "image.png=@image.png" 
  -F "data.csv=@data.csv"

**Response:**
Structured data (JSON or JSON array) matching the format specified in questions.txt.  
Plots are returned as Base64-encoded strings (data:image/png;base64,...).

## Architecture

1. **Request Handling** – FastAPI endpoint receives questions.txt and optional attachments.  
2. **Task Parsing** – LLM interprets the analysis instructions.  
3. **Data Ingestion** – Loads provided datasets or fetches data from specified sources (e.g., Wikipedia, S3).  
4. **Processing** – Uses Python data libraries (pandas, 
umpy, duckdb, eautifulsoup4, equests) for analysis.  
5. **Visualization** – Generates plots with matplotlib/seaborn, encodes them to Base64.  
6. **Response Generation** – Returns JSON in the requested structure.

## Installation

git clone https://github.com/<your-repo>.git  
cd data-analyst-agent  
pip install -r requirements.txt

## Running Locally

uvicorn main:app --host 0.0.0.0 --port 8000

Test locally:

curl "http://127.0.0.1:8000/api/" 
  -F "questions.txt=@examples/question_wiki.txt" 
  -F "data.csv=@examples/data.csv"

## Deployment

You can deploy to any platform (e.g., AWS, Render, Railway, Fly.io). Ensure the endpoint is publicly accessible.

## License

MIT
