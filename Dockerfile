FROM python:latest
COPY . /app
WORKDIR /app
CMD [ "pip", "install", "selenium" ]