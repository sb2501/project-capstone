import pika
import shutil
import os
import subprocess
import time
import sys

IP=os.environ["MASTER_IP"] or 'localhost'



#function for input check
def find(name, path):
	count=0
    	for root, dirs, files in os.walk(path):
        	if name in files:
			count+=1
	
	return(count)

def callback(ch, method, properties, body):
	ch.basic_ack(delivery_tag=method.delivery_tag)
	input = body[0:body.find(':')]
	output = body[body.find(':')+1:len(body)]
	temp = input[input.rfind('/')+1:len(input)]	
	temp2 = input[0:input.rfind('/')]	

	if(len(input) > 0):
		output_file = input[0:len(input)-3] + 'mp4'
		output_file = temp[0:len(temp)-3] + 'mp4'
		#start input check
		
		if((find(output_file, output) <1) and (find(output_file, temp2) < 1)):
			cmd = "ffmpeg -i " + input + " -preset slow -map_metadata 0:g " + output_file + " -y"
			#Transcode Here
			start=time.time()
			try:
				subprocess.check_call(cmd,shell=True)
				shutil.move(output_file,output)
				shutil.move(input, "../Original")
				#os.remove(input)
				print("Video transcoded")
			except subprocess.CalledProcessError:
				#Re-send job to queue here
				os.remove(output_file)
				resend="python master.py " + body
				subprocess.check_call(resend, shell=True)
				print("Video couldn't be transcoded!")
			
			end=time.time()
			total=end-start
			
			print("it took ", total, "seconds")
		else:
			print("Output file with same name detected")




try:
	connection = pika.BlockingConnection(pika.ConnectionParameters(host=IP,blocked_connection_timeout=None))
	channel = connection.channel()

	channel.queue_declare(queue='vids', durable=True)

	channel.basic_qos(prefetch_count=1)
	channel.basic_consume(callback, queue='vids')
	channel.start_consuming()
	
except pika.exceptions.ChannelClosed:
	script = "python " + os.path.basename(sys.argv[0])
	#Run new subprocess and terminate current process
	suprocess.check_call(script, shell=True)
	sys.exit()
