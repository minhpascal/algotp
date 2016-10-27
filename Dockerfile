FROM continuumio/anaconda3

MAINTAINER Yohannes Haile

RUN apt-get -y install python3
RUN apt-get -y update
RUN apt-get -y install python3-pip --fix-missing


#WORKDIR /usr/local/lib/python3.4/dist-packages/
# Copy the application folder inside the container
RUN mkdir /atp
ADD . /atp/
WORKDIR /atp

RUN python3 setup.py develop
WORKDIR /atp/atp

# Get pip to download and install requirements:
#


CMD ["python3","tests.py"]
