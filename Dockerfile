FROM python:3.9-buster

RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN apt-get update && apt-get install -y build-essential lsof  && pip install -r /code/requirements.txt

EXPOSE 1010

#ENTRYPOINT ["bash", "run.sh"]
