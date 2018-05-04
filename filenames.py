import os
import sys
import subprocess

names=os.listdir(sys.argv[1]) #gets file names for all files in passed in directory

#loops through names array to start job for each file
for file in names:
	temp="python Incomplete/master.py " + "../" + sys.argv[1] + "/" +file + ":../Complete" #creates string for the master.py script on each file name
	subprocess.call(temp, shell=True) #runs the temp string
	#print("python Incomplete/master.py " + sys.argv[1] + "/" +file + ":../Complete") #used to check temp string