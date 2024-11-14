FROM docker.io/library/python:3.12-alpine

COPY /app /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
