FROM python:3.9-alpine

RUN apk update

WORKDIR /spotify

COPY requirements.txt /spotify

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]
