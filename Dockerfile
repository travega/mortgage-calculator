FROM python:alpine2.7
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip; pip install -r requirements.txt
