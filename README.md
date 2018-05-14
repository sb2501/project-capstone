Video Transcoding with Docker and Rabbitmq
=============================

Current Docker Hub image
(https://hub.docker.com/r/sboyd001/rabbitmq-project/)

How to use Dockerfile
----------------------------

### Build docker master node image (while in the directory)

```bash
docker .
```

### Build docker consumer node image (while in the directory)

To build the consumer node, the IP address of the master is passed in as an environment variable when building consumer

```bash
docker build --build-arg MASTER_IP=[MASTER_COMPUTER_IP] .
```

### Running containers

LOCAL_FILE_PATH - this is the folder location of the cloned GitHub repo
NAME - desired name of the container
IMAGE_NAME- name of the image from the built dockerfile

Job submitter:

```bash
docker run -d -v [LOCAL_FILE_PATH]:/home --name=[NAME] [IMAGE_NAME] 
--Use master build from Master folder
```

Consumer:

```bash
docker run -d -v [LOCAL_FILE_PATH]:/home --name=[NAME] [IMAGE_NAME_HERE] 
--Use consumer build from Consumer folder
```

Running jobs
----------------------------

Submitting jobs:

Option 1:

Steps:

1) Get into jub submitter container:

```bash
docker exec -it [CONTAINER_NAME] bash
```

2)Change directory to Incomplete folder where the scripts are
```bash
cd home/Incomplete/
```

3)Run transcode on specficfile
```bash
python master.py [FILE_NAME:/[OUTPUT_FOLDER_PATH]
```

Option 2 (sending folder of video files): 
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

Running a new file
```bash
When a new file is submited by the master, the job is pushed into the queue and the consumer runs the job. The consumer will transcode the video and then move the newly formatted video into the desired output folder that was passed in by the master. The consumer will then move the original file from the video folder to a folder called "original" to ensure that the video file does not get deleted. After the cideo is transcoded, it will print a message saying that the video has been transcoded and how long the process took. 
```

Running a repeated file
```bash
When a file that already has been transcoded is pushed into the queue by the master, when picked up by the consumer the consumer script runs a check to see if a file with the same name is already in the output folder. If a file with the same name is found, it will print a message saying that the video has already been transcoded, and will not run the transcoding part of the consumer script. Doing this removes the job from the queue and also removes the video from the video folder. 
```

If a job fails
```bash
If the transcode process fails while running the FFMPEG command, it will be put back into the queue and will be picked up by another node.
```
