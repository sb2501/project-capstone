import os
import subprocess

IP = os.environ["MASTER_IP"]
subprocess.call("touch master_ip.txt", shell=True)
subprocess.call("echo " + IP + " >> master_ip.txt", shell=True)


