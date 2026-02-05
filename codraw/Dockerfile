FROM python:3.12-slim
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip setuptools wheel
ENV PATH="/py/bin:$PATH"
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn google-cloud-storage
COPY . .
ENV PYTHONPATH=/app
CMD ["daphne", "-b", "0.0.0.0", "-p", "8080", "codraw.asgi:application"]
