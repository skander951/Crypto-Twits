FROM python:3.11-slim
WORKDIR /app
COPY predict.py .
RUN pip install pandas scikit-learn joblib
CMD ["python", "predict.py"]