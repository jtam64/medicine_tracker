FROM python:latest

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 1554

CMD [ "flask", "run","--host","0.0.0.0","--port","5000"]