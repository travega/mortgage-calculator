FROM python:alpine3.7
COPY . /app
WORKDIR /app
RUN echo "DONE!"
