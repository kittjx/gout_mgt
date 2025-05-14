FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN apt update && \
    pip install --upgrade pip && \
    pip install django pymysql cryptography djangorestframework django-cors-headers

EXPOSE 8000

CMD [ "bash" ]

