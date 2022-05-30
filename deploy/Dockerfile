FROM python:3.9-slim

WORKDIR /
COPY ./deploy/requirements.txt /
RUN pip install -r requirements.txt --no-cache-dir
COPY ./src .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]