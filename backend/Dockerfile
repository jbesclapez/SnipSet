# Use an official Python runtime as a parent image
FROM python:3.9

# Install netcat-openbsd for the entrypoint script
RUN apt-get update && apt-get install -y netcat-openbsd

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose port 5000
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app

# Add this line to set PYTHONPATH
ENV PYTHONPATH=/app

# Use the entrypoint script to start the application
ENTRYPOINT ["/app/entrypoint.sh"]

