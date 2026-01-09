# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port (informative, Railway uses PORT env var)
# EXPOSE 8000

# Define environment variable
ENV FHIR_BASE_URL="http://172.20.10.14:8080/fhir"

# Run the application
CMD ["python", "main.py"]
