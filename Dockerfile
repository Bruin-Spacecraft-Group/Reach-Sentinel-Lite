# Dockerfile

FROM python:3.7
ENV PYTHONUNBUFFERED 1

RUN pip install virtualenv
RUN  virtualenv -p python3 reachSentinelLite
COPY reachSentinelLite/ reachSentinelLite/

ENV PATH /reachSentinelLite/bin/:$PATH

RUN . /reachSentinelLite/bin/activate
RUN pip install -r reachSentinelLite/dumreqs.txt
WORKDIR reachSentinelLite/

EXPOSE 8000
STOPSIGNAL SIGTERM
CMD python3 manage.py runserver 0.0.0.0:8000
