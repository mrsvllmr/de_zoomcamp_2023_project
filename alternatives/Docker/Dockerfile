# used to build images (which then later lead to an actual container)
# process: Manifest/Dockerfile -> image -> container
# uses the docker build command
FROM python:3.9.1

RUN apt-get update
RUN apt-get install wget
RUN pip install -r requirements.txt

WORKDIR /app
#COPY ingest_data.py ingest_data.py 

#ENTRYPOINT [ "python", "ingest_data.py" ]