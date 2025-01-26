# Use a base image with Python 3.11
FROM python:3.11-slim

# Set the working directory
WORKDIR /projects/buletin-contract

# Install necessary libraries
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set the entrypoint to your application
CMD ["python", "app.py"]
