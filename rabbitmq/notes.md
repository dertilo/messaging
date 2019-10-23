

* We could avoid that if we were sure that the queue already exists. For example if send.py program was run before. But we're not yet sure which program to run first. In such cases it's a good practice to repeat declaring the queue in both programs.
* By default, RabbitMQ will send each message to the next consumer, in sequence. On average every consumer will get the same number of messages. This way of distributing messages is called round-robin. 

* we've already defined a queue called hello which is not durable. RabbitMQ doesn't allow you to redefine an existing queue with different parameters and will return an error
* prefetch_count=1 setting. This tells RabbitMQ not to give more than one message to a worker at a time.

### Remote Procedure Call or RPC.