FROM python:3.6-slim

# RUN apt-get update && apt-get install -y bash libpq-dev gcc

COPY requirements.txt /app/requirements.txt

COPY audienceoverlap/ /app/audienceoverlap

WORKDIR /app

# ADD . /app

RUN pip install -r requirements.txt

# RUN export BOKEH_SECRET_KEY=$(bokeh secret); echo $BOKEH_SECRET_KEY>/app/secret.txt

USER nobody
