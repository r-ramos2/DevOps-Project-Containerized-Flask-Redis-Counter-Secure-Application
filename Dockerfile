# Stage 1: Build Stage
FROM python:3.11-alpine as builder

WORKDIR /app
RUN apk add --no-cache gcc musl-dev libffi-dev
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Final Stage
FROM python:3.11-alpine

WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl --fail http://localhost:5000/ || exit 1

CMD ["python", "app.py"]
