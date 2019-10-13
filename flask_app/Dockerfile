FROM python:2.7-slim

WORKDIR /app

COPY ./app /app
#this copies the /app directory from the host system to the /app folder withion the container, this can be checked by entering the container whilst its running

RUN pip install -r /app/requirements.txt

#this exposes port 5000 on the container, the port 5000 exposed on the container is automatically mapped on the exposed port on the app as specified in app.py
EXPOSE 5000
#when running the docker container do -p 5000:5000, this maps the host port to the container port (host:container)
#this is obvious from the port info when the app is runnign which shows 0.0.0.0:5000->5000/tcp meaning traffic from all ports on host(0.0.0.0) go through port 5000 of the container(1st number) and then through 5000(second number) of the app
CMD [ "python", "./app.py"]

