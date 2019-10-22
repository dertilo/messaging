'''
inspired by https://github.com/rabbitmq/rabbitmq-tutorials/blob/master/python/rpc_server.py
'''
import sys
import time

import pika
from pikautil.pika_util import build_blocking_connection_with_retry

with build_blocking_connection_with_retry() as connection:
    with connection.channel() as channel:

        channel.queue_declare(queue='rpc_queue')

        def on_request(ch, method, props, body):
            n = int(body)
            time.sleep(n)
            print('working on task: %s'%props.correlation_id)
            sys.stdout.flush()

            response = "task %s took %d seconds" % (props.correlation_id, n)

            ch.basic_publish(exchange='',
                             routing_key=props.reply_to,
                             properties=pika.BasicProperties(correlation_id = props.correlation_id),
                             body=response)
            ch.basic_ack(delivery_tag=method.delivery_tag)


        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

        print(" [x] Awaiting RPC requests")
        sys.stdout.flush()
        channel.start_consuming()