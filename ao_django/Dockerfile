FROM python:3.6


# RUN mkdir -p /static_volume/static/
RUN mkdir -p /opt/sevices/djangoapp/src
WORKDIR /opt/sevices/djangoapp/src
COPY . /opt/sevices/djangoapp/src
RUN pip install -r requirements.txt
RUN python manage.py migrate
RUN python manage.py collectstatic --no-input
VOLUME ["/static"]
COPY static/ /static/
COPY static/home/ /static/home/
COPY static/css/ /static/css/
COPY static/js/ /static/js/
RUN ls -la /static/*
# CMD ["python", "manage.py", "runserver"]
# VOLUME ["/opt/ao_django/collected_static"]