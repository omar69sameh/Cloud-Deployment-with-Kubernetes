FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY recidivism_model.pkl .
COPY label_encoders.pkl .
COPY feature_names.pkl .

EXPOSE 5000

CMD ["python", "app.py"]