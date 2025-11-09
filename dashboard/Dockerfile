# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy the dashboard app
COPY app.py .

# Install required Python packages
RUN pip install pandas dash plotly flask python-dotenv

# Mount data volume
VOLUME ["/data"]

# Expose port
EXPOSE 8050

# Run the dashboard
CMD ["python", "app.py"]
