FROM python:3.12

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE="weather_app.config.settings.deployed"
ENV JWT_PRIVATE_KEY="./rsa-private-key.pem"
ENV JWT_PUBLIC_KEY="./rsa-public-key.pem"
ENV PYTHONPATH="${PYTHONPATH}:/src"

COPY ./src/ /src/
COPY ./requirements.txt /src/requirements.txt
WORKDIR /src/weather_app

RUN openssl genrsa -out rsa-private-key.pem 2048
RUN openssl rsa -in rsa-private-key.pem -pubout -outform PEM -out rsa-public-key.pem

# install dependencies
RUN pip install -r /src/requirements.txt
