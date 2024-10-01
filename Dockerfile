# Use an official Python runtime as a parent image
FROM python:3.10.12

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8050 for the Dash app
EXPOSE 8050

# Define environment variable to disable Dash debug mode in production
ENV DASH_DEBUG_MODE=False

# Run the app when the container launches
CMD ["gunicorn", "--bind", "0.0.0.0:8050", "app:server"]
