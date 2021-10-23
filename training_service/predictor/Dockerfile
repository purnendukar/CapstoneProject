FROM python:3.8-slim

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV DISPLAY=:99

# Install apt dependencies
#RUN apt update && apt install -y openjdk-11-jdk && export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64



# Install requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt && python -m nltk.downloader punkt && python -m nltk.downloader stopwords

COPY . /app

ENTRYPOINT python wsgi.py