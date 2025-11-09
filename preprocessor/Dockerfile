FROM python:3.11-slim
WORKDIR /app

COPY merge_data.py .
RUN pip install pandas

VOLUME ["/data"]
CMD ["python", "merge_data.py"]
