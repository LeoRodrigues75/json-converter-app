# Use an official lightweight Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Command to run the application using Gunicorn
# This tells Cloud Run how to start your web server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]