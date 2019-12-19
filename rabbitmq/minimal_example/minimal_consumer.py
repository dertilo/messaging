#!/usr/bin/env python
import sys

import pika
import time
from pikautil.pika_util import build_blocking_connection_with_retry


if __name__ == "__main__":
    connection = build_blocking_connection_with_retry()
    channel = connection.channel()

    channel.queue_declare(queue="task_queue", durable=True)
    sys.stdout.flush()

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        time.sleep(body.count(b"."))
        print(" [x] Done")
        sys.stdout.flush()
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_message_callback=callback, queue="task_queue")

    try:
        channel.start_consuming()
    finally:
        connection.close()
