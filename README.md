Video Transcoding with Docker and Rabbitmq
=============================

Current Docker Hub image
(https://hub.docker.com/r/sboyd001/rabbitmq-project/)

How to use Dockerfile
----------------------------

apt-get commands added to dockerfile
```bash
apt-get install python
apt-get install python-pip
apt-get install ffmpeg
pip install pika
```

### Build docker image (while in the directory)

```bash
docker build .
```

### Running containers

Job submitter:

```bash
docker run -d -v [LOCAL_FILE_PATH]:/home --name=[NAME] [IMAGE_NAME_HERE] 
--Use master build from Master folder
```

Consumer:

```bash
docker run -d -v [LOCAL_FILE_PATH]:/home --name=[NAME] [IMAGE_NAME_HERE] 
--Use consumer build from Consumer folder
```

Running jobs
----------------------------

Submitting job:

Option 1:

Steps:

1) Get into jub submitter container:

```bash
docker exec -it [CONTAINER_NAME] bash
```

2)Change directory to Incomplete folder
```bash
cd home/Incomplete/
```

3)Run transcode on file
```bash
python master.py [FILE_NAME:/[OUTPUT_FOLDER_PATH]
```

Option 2: 
```bash
python filenames.py [NAME_OF_VIDEO_FOLDER]
```

Consuming jobs:

Steps:

1) Get into consumer submitter container:

```bash
docker exec -it [CONTAINER_NAME] bash
```

2)Change directory to Incomplete folder
```bash
cd home/Incomplete/
```

3)Run consumer script
```bash
python consumer.py
```

4)Stop consumer script
```bash
ctl+c
```

Clearing the queue
----------------------------
```bash
rabbitmqctl purge_queue vids
```

Description:
----------------------------
Passing in environment variable when building consumer
docker --build-arg MASTER_IP=10.11.131.243 .

Running a new file
```bash
When a new file is submited by the master, the job is pushed into the queue and the consumer runs the job. The consumer will transcode the video
and then move the newly formatted video into the desired output folder that was passed in by the master. The consumer will then delete the original 
file from the Incomplete folder and print a message saying that the video has been transcoded and how long the process took. 
```

Running a repeated file
```bash
When a file that already has been transcoded is pushed into the queue by the master, when picked up by the consumer the consumer script runs a 
check to see if a file with the same name is already in the output folder. If a file with the same name is found, it will print a message saying
that the video has already been transcoded, and will not run the transcoding part of the consumer script. Doing this removes the job from the queue 
and also removes the video from the Incomplete folder. 
```


