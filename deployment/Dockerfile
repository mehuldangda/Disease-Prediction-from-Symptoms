# Dockerfile for Streamlit Deployment / Hugging Face Spaces
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Train ML models during container build if missing
RUN python -c "import os; os.path.exists('saved_model/random_forest.joblib') or __import__('ml.train').train.ModelTrainer().train_all()"

# Expose port 8501 (Streamlit default) or 7860 (Hugging Face Spaces)
EXPOSE 7860
EXPOSE 8501

# Run Streamlit application
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0", "--server.headless=true"]
