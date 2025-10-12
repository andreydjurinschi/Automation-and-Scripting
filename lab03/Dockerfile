FROM python:3.10
RUN apt-get update && apt-get install -y cron
WORKDIR /app
COPY currency_exchange_rate.py cronjob entrypoint.sh ./

RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install requests

RUN chmod +x /app/entrypoint.sh
RUN crontab /app/cronjob

ENTRYPOINT ["/app/entrypoint.sh"]
