# Use an OpenShift-compatible Python image as a base
FROM registry.access.redhat.com/ubi8/python-39

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Set the entry point to run the Flask application
ENTRYPOINT ["python", "app.py"]
