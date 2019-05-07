FROM python:alpine3.7
COPY . /app
WORKDIR /app
RUN \
 apk add --no-cache python postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc python-dev musl-dev postgresql-dev && \
 python -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps
