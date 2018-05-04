import pika
import sys

#IP=os.environ["MASTER_IP"]

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()



channel.queue_declare(queue='vids', durable= True)

message = ' '.join(sys.argv[1:]) or "\temp.mp4"

channel.basic_publish(exchange='',routing_key='vids',body=message,properties=pika.BasicProperties(delivery_mode=2))

print(" [x] Sent %r" % message)
connection.close()

