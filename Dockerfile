FROM python:3.6
RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi
COPY /root/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY /root /app
RUN chown -R uwsgi /app
COPY uwsgi.sh /uwsgi.sh
RUN chmod +x /uwsgi.sh