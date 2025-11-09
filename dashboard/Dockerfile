FROM python:3.11-slim
WORKDIR /app
COPY app.py .
RUN pip install pandas dash plotly flask
VOLUME ["/data"]
CMD ["python", "app.py"]
