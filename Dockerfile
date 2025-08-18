# Use Python 3.11 slim base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app files
COPY . .

# Ensure output is unbuffered (logs visible immediately)
ENV PYTHONUNBUFFERED=1

# Expose port for FastAPI
EXPOSE 8000

# Start FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
