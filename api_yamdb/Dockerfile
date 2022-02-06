FROM python:3.7-slim

COPY ./ /app

WORKDIR /app

RUN pip install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:5000" ]