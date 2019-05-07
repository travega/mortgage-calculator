FROM python:alpine3.7
COPY . /app
WORKDIR /app
RUN pip2 install -r requirements.txt
