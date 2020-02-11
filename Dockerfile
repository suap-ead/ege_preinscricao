FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update && \
    apk add postgresql-libs && \
    apk add --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
    pip install psycopg2-binary && \
    apk --purge del .build-deps gcc python3-dev musl-dev postgresql-dev

RUN python -m pip install Django

RUN mkdir /pre_inscricao
WORKDIR /pre_inscricao

COPY . /pre_inscricao
RUN pip install -r requirements.txt

# RUN python manage.py makemigrations
# RUN python manage.py migrate
# RUN python manage.py createsuperuser

EXPOSE 8000