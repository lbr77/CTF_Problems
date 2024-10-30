FROM python:3.8-alpine
RUN apk add --no-cache socat
COPY flag /flag
WORKDIR /app
COPY src /app/src

CMD ["socat","TCP-LISTEN:1145,reuseaddr,fork", "EXEC:python /app/src/server.py"]