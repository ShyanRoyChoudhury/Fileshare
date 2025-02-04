FROM python:3.13

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
COPY . /app/
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8443
CMD ["gunicorn", "--certfile=certs/server.crt", "--keyfile=certs/server.key", "--bind", "0.0.0.0:8443", "backend.wsgi:application"]
