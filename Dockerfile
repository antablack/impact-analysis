FROM python:3.8

WORKDIR /usr/src/app

#RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

