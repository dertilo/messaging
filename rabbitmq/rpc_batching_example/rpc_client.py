import random
import sys

import numpy
import pika
import uuid

from pikautil.pika_util import build_blocking_connection_with_retry

counter = 0


def get_id():
    global counter
    counter += 1
    return str(counter)  # just for readablity in this examle
    # return str(uuid.uuid4())


if __name__ == "__main__":

    with build_blocking_connection_with_retry() as connection:
        with connection.channel() as channel:
            channel.queue_declare(queue="rpc_queue")

            result = channel.queue_declare(queue="", exclusive=True)
            callback_queue = result.method.queue

            id_tasks = [(get_id(), k) for k in range(8)]
            random.shuffle(id_tasks)

            for eid, task in id_tasks:
                channel.basic_publish(
                    exchange="",
                    routing_key="rpc_queue",
                    properties=pika.BasicProperties(
                        reply_to=callback_queue, correlation_id=eid
                    ),
                    body=str(task),
                )

            for method_frame, properties, body in channel.consume(
                queue=callback_queue, auto_ack=True
            ):
                print("task-id: %s; result: %s" % (properties.correlation_id, body))
                sys.stdout.flush()
