# Use a base image with Python 3.11
FROM python:3.11-slim

# Set the working directory
WORKDIR /projects/buletin-contract

# Install necessary libraries and Tesseract OCR
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Ensure Tesseract is in the PATH
ENV PATH="/usr/bin/tesseract:${PATH}"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install gunicorn
RUN pip install gunicorn

# Copy the application code
COPY . .

# Use gunicorn as the entrypoint