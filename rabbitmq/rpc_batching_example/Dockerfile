FROM python:3.6
RUN pip install -U pika
COPY . /root/messaging
RUN pip install scipy
RUN cd /root/messaging && pip install .
WORKDIR /root