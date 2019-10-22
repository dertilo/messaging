import sys
import time

import pika
from pikautil.pika_util import build_blocking_connection_with_retry
from util.util_methods import iterable_to_batches

def process_batch(batch):
    bodies = [int(body) for method_frame, properties, body in batch]
    n = sum(bodies)
    time.sleep(n)
    return ["task %s batch took: %d seconds" % (p.correlation_id, n) for m, p, b in batch]

batch_size=3

with build_blocking_connection_with_retry() as connection:
    with connection.channel() as channel:

        channel.queue_declare(queue='rpc_queue')
        channel.basic_qos(prefetch_count=batch_size)
        for batch in iterable_to_batches(channel.consume(queue='rpc_queue',inactivity_timeout=1),batch_size=batch_size):
            batch = [b for b in batch if all([x is not None for x in b])]
            if len(batch)>0:
                results = process_batch(batch)
                for (method_frame, properties, body),result in zip(batch,results):
                    print('delivered: %s'%properties.correlation_id); sys.stdout.flush()
                    channel.basic_publish(exchange='',
                                     routing_key=properties.reply_to,
                                     properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                                     body=result)

                tag = batch[-1][0].delivery_tag
                print('acknowledged up to %s'%str(tag)); sys.stdout.flush()
                channel.basic_ack(delivery_tag=tag, multiple=True)
            else:
                print('idle');  sys.stdout.flush()


        print(" [x] Awaiting RPC requests")
        sys.stdout.flush()
        channel.start_consuming()