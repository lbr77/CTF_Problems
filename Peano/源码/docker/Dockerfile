FROM python:3.7-slim-bookworm   

WORKDIR /app

COPY app/* /app/
RUN pip install numpy && pip install pillow && pip install qrcode
RUN apt update && apt install -y socat
CMD ["sh","run.sh"]

EXPOSE 9999