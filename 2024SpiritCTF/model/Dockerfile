FROM python:3.10-slim
RUN apt-get update && apt-get install -y socat
RUN pip install jinja2 && pip install torch==2.5.0+cpu -i https://download.pytorch.org/whl/cpu
COPY flag /flag
WORKDIR /app
COPY src /app/src

CMD ["socat","TCP-LISTEN:1145,reuseaddr,fork", "EXEC:python /app/src/server.py"]