FROM ubuntu:18.04

RUN apt-get update && apt-get install -y python3 python3-pip

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3"]

CMD ["app.py"]

