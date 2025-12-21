# Using an offical lightweight python image
From python:3.10-slim

# Setting working directory
WORKDIR /app

# Copying dependency list 
COPY requirements/txt .

# Install system dependencies
RUN apt-get update && apt-get install -y \ 
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the project
COPY . .

# FastAPI port
EXPOSE 8000

# Run your FastAPI app
CMD ["uvicorn","app.main:app", "--host", "0.0.0.0","--port","8000"]