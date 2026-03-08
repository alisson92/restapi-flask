FROM python:3.12.13-alpine3.23

EXPOSE 5000

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY wsgi.py .
COPY config.py .
COPY application application

CMD ["python", "wsgi.py"]
