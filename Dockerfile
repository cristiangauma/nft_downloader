FROM python:alpine
COPY . /app/
WORKDIR /app/

RUN pip3 install pipenv && \
    pipenv install