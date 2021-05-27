FROM python:3.7

WORKDIR /app/app

WORKDIR /app

COPY /app/requirements.txt /app/app/

RUN ls /app/app

RUN pip install -r /app/app/requirements.txt

WORKDIR  /app/app/data

WORKDIR /app

COPY /app/data /app/app/data

WORKDIR /app/app/forms

WORKDIR /app

COPY /app/forms /app/app/forms

WORKDIR /app

WORKDIR /app/app/templates

WORKDIR /app

COPY /app/templates /app/app/templates

COPY /app/app.py /app/app

WORKDIR /app/app/models

WORKDIR /app

COPY /app/models /app/app/models 

#this exposes port 5000 on the container, the port 5000 exposed on the container is automatically mapped on the exposed port on the app as specified in app.py

EXPOSE 5000

#when running the docker container do -p 5000:5000, this maps the host port to the container port (host:container)
#this is obvious from the port info when the app is runnign which shows 0.0.0.0:5000->5000/tcp meaning traffic from all ports on host(0.0.0.0) go through port 5000 of the container(1st number) and then through 5000(second number) of the app

WORKDIR /app/app

CMD [ "python", "app.py"]
