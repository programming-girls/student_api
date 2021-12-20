FROM python:3.9.1-alpine3.12

ENV PYTHONUNBUFFERED 1

COPY . /STUDENT_API

WORKDIR /STUDENT_API

RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev linux-headers libffi-dev libxml2-dev

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD gunicorn gettingstarted.wsgi --log-file -
