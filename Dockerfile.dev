FROM python:3.11.1-slim

WORKDIR /usr/src/app

COPY . .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN apt update
RUN apt install -y netcat

RUN sed -i 's/\r$//g' /usr/src/app/scripts/start.sh
RUN chmod +x /usr/src/app/scripts/start.sh

ENTRYPOINT ["/usr/src/app/scripts/start.sh"]
