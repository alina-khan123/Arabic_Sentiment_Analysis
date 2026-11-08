# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
# Note: we assume the Dockerfile is in the project root
COPY dashboard/requirements.txt .

# Install any needed packages specified in requirements.txt
# Using --no-cache-dir to keep the image small
RUN pip install --no-cache-dir -r requirements.txt

# Copy the dashboard directory contents into the container at /app/dashboard
COPY dashboard/ ./dashboard/

# Copy the data file needed by the application (it lives one level above dashboard)
COPY data_full_clean.csv .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
# We run it from the root directory so the relative path logic in app.py works
CMD ["python", "dashboard/app.py"]
