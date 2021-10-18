FROM python:latest

ADD . /app

WORKDIR /app

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt
EXPOSE 8080
CMD python3 main.py
