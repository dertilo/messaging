import time

import pika


def build_blocking_connection_with_retry(
    host="rabbitmq", num_retries=9, sleep_seconds=2
):
    connection = None
    for k in range(num_retries):
        time.sleep(sleep_seconds)
        print("try to connect: %d" % k)
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
            break
        except:
            pass

    if connection is None:
        raise Exception("could not connect to rabbitmq")
    else:
        return connection
