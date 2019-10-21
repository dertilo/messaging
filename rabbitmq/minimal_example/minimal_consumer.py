#!/usr/bin/env python
import sys

import pika
import time

def setup_connection():
    connection = None
    for k in range(9):
        time.sleep(3)
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

    channel.queue_declare(queue='task_queue', durable=True)
    sys.stdout.flush()

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        time.sleep(body.count(b'.'))
        print(" [x] Done")
        sys.stdout.flush()
        ch.basic_ack(delivery_tag = method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_message_callback=callback,
                          queue='task_queue')

    try:
        channel.start_consuming()
    finally:
        connection.close()


