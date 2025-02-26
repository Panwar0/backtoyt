FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["gunicorn", "--worker-class", "eventlet", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
