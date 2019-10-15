FROM python:3.6

WORKDIR /app

COPY ./app /app

RUN pip install -r /app/requirements.txt

CMD ["python", "/app/mongo_writer.py"]
