FROM python:3.7-alpine
WORKDIR /root/
RUN apk add --update --no-cache ffmpeg
RUN pip install watchdog
COPY watch.py .
CMD python watch.py
