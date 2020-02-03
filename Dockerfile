# Dockerfile

FROM python:3.7
ENV PYTHONUNBUFFERED 1

RUN pip install virtualenv
RUN mkdir reachSentinelLite
COPY reachSentinelLite/ reachSentinelLite/

ENV PATH /reachSentinelLite/bin/:$PATH


RUN . /reachSentinelLite/bin/activate
RUN pip install -r reachSentinelLite/dumreqs.txt
WORKDIR reachSentinelLite/


CMD python3 manage.py
#CMD python3 main.py
