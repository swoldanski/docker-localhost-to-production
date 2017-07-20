FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1
ENV APP_DIR /code
WORKDIR $APP_DIR

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY src $APP_DIR

CMD python app.py