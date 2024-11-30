# Use official Python image
FROM python:3.12-slim

# Choose working dir
WORKDIR /app

# Install system requirments
RUN apt-get update && apt-get install -y libpq-dev unzip && rm -rf /var/lib/apt/lists/*

# Add requirements file to image
COPY requirements.txt  .

# Install python libraries
RUN --mount=type=cache,mode=0755,target=/root/.cache/pip pip install -r requirements.txt

# Create a group and user
RUN chmod 777 /app

# Add Python enviroments
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Run application
CMD ["python", "webhook.py"]