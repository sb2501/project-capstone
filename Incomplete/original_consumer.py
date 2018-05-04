import pika
import shutil
import os
import subprocess
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.17.0.3'))
channel = connection.channel()

channel.queue_declare(queue='vids', durable=True)


def callback(ch, method, properties, body):
	input = body[0:body.find(':')]
	output = body[body.find(':')+1:len(body)]
	
	if(len(input) > 0):
		output_file = input[0:len(input)-3] + 'mp4'
		cmd = "ffmpeg -i " + input + " -preset slow -map_metadata 0:g " + output_file
		#Transcode Here
		start=time.time()
		subprocess.call(cmd,shell=True)
		shutil.move(output_file,output)
		os.remove(input)
		end=time.time()
		total=end-start
	print("Video transcoded")
	print("it took ", total, "seconds")
	ch.basic_ack(delivery_tag=method.delivery_tag)
	


channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='vids')
channel.start_consuming()
