FROM python:alpine3.7.2
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip; pip install -r requirements.txt
