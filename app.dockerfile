FROM python:3.8-bullseye
COPY ./ /app
WORKDIR /app
RUN pip3 install -r requirenments.txt