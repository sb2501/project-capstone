import pika
import shutil
import os
import subprocess
import time
import sys
import string

IP = os.environ["MASTER_IP"]
connection = pika.BlockingConnection(pika.ConnectionParameters(host=IP))
channel = connection.channel()

channel.queue_declare(queue='vids', durable=True)

#function for input check
def find(name, path):
	count=0
	#looks for file with same name in the completed folder
    	for root, dirs, files in os.walk(path):
        	if name in files:
			count+=1
	
	return(count)

def callback(ch, method, properties, body):
	#Takes queue  message passed in to body variable and splits string at the first occurence of ':' to get the input path and output directory
	input = body[0:body.find(':')]
	output = body[body.find(':')+1:len(body)]
	
	if(len(input) > 0):
		output_file = input[0:len(input)-3] + 'mp4'

		#start input check
		#checks if file has been transcoded
		if(find(output_file, output) <1):
			cmd = "ffmpeg -i " + input + " -preset slow -map_metadata 0:g " + output_file
			#Transcode Here
			start=time.time() #used starts timer
			#System call to ffmpeg
			subprocess.call(cmd,shell=True)
			#Move trancoded video into output directory
			shutil.move(output_file,output)
			#Remove input file from incomplete folder
			os.remove(input)
			end=time.time() #ends timer
			total=end-start #gets total time taken to transcode video
			print("Video transcoded")
			print("it took ", total, "seconds")
		else:
			print("Output file with same name detected") #if same file name found, message is printed
		
	
	#Send ACK to master 
	ch.basic_ack(delivery_tag=method.delivery_tag)
	


channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='vids')
channel.start_consuming()

