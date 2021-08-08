import pika


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='payment',
                         exchange_type='x-delayed-message',
                         arguments={"x-delayed-type":"direct"})

message = 'Hello World! 10 detik'
channel.basic_publish(exchange='payment',
                      routing_key='scheduler',
                      properties=pika.BasicProperties(headers={'x-delay': 10000}),
                      body=message)
connection.close()