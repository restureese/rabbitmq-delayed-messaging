import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='payment',
                         exchange_type='x-delayed-message',
                         arguments={"x-delayed-type":"direct"})

result = channel.queue_declare(queue='payment',exclusive=True)
queue_name = result.method.queue


channel.queue_bind(exchange='payment',
                   queue=queue_name,
                   routing_key='scheduler')


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


channel.basic_consume(queue_name, callback)
channel.start_consuming()