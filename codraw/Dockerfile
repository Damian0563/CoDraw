FROM python:alpine3.21
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev
WORKDIR /
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn
RUN apk del gcc musl-dev python3-dev libffi-dev
COPY . .
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080","--chdir", "/app" "codraw.wsgi:application"]
