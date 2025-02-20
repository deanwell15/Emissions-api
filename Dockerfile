FROM python:3.8-alpine
ENV APP /api
RUN mkdir $APP
WORKDIR $APP

COPY requirements.txt .
RUN apk add --no-cache --virtual .build-deps gcc make musl-dev libressl libffi libressl-dev libffi-dev openssl-dev
RUN pip3 install -r requirements.txt
RUN apk del .build-deps gcc make musl-dev

COPY .$APP/* ./

CMD python3 api.py