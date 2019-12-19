#!/usr/bin/env python
from time import sleep, time

import pika
import sys

from pikautil.pika_util import build_blocking_connection_with_retry

if __name__ == "__main__":
    connection = build_blocking_connection_with_retry()
    channel = connection.channel()

    q = channel.queue_declare(queue="task_queue", durable=True)

    counter = 0
    for counter in range(9):
        counter += 1
        message = "%d_" % counter + "." * (1 + (counter % 2 == 0))
        channel.basic_publish(
            exchange="",
            routing_key="task_queue",
            body=message,
            properties=pika.BasicProperties(delivery_mode=2),  # make message persistent
        )
        print(" [x] Sent %r" % message)

    connection.close()
