#!/usr/bin/env python
from time import sleep, time

import pika
import sys
sleep(10)

def setup_connection():
    connection = None
    for k in range(9):
        sleep(3)
        print('try to connect: %d' % k)
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='rabbitmq'))
            break
        except:
            pass

    if connection is None:
        raise Exception('could not connect to rabbitmq')
    else:
        return connection

if __name__ == '__main__':
    connection = setup_connection()
    channel = connection.channel()

    q = channel.queue_declare(queue='task_queue', durable=True)

    counter=0
    for counter in range(9):
        counter+=1
        message = '%d_'%counter+'.'*(1+(counter%2==0))
        channel.basic_publish(exchange='',
                              routing_key='task_queue',
                              body=message,
                              properties=pika.BasicProperties(
                                  delivery_mode=2,  # make message persistent
                              ))
        print(" [x] Sent %r" % message)

    connection.close()