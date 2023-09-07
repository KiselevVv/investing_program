FROM python:3.7-slim

WORKDIR /app

COPY . .

RUN pip install -r /app/requirements.txt --no-cache-dir

EXPOSE 5000

CMD ["python", "run.py"]
