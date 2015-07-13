FROM ubuntu:14.04
MAINTAINER Boyan Tabakov <boyan.tabakov@futurice.com>

# Configure apt to automatically select mirror
RUN echo "deb mirror://mirrors.ubuntu.com/mirrors.txt trusty main restricted universe\n\
deb mirror://mirrors.ubuntu.com/mirrors.txt trusty-updates main restricted universe\n\
deb mirror://mirrors.ubuntu.com/mirrors.txt trusty-security main restricted universe" > /etc/apt/sources.list

# Add nginx repo
RUN apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62
RUN echo "deb http://nginx.org/packages/ubuntu/ trusty nginx" >> /etc/apt/sources.list
RUN apt-get update && apt-get install -y nginx

# Common packages
RUN apt-get update && apt-get install -y \
	libpq-dev \
	python \
	python-pip \
	python-dev \
	supervisor

# Node.js
# Download node.js from Futurice CDN S3 bucket over SSL. Files there have verified checksums. Official site downloads are over insecure connection.

ENV NODE_VERSION 0.10.36
RUN apt-get update && apt-get install -y wget \
	&& wget --quiet -O /tmp/node.tar.gz https://s3-eu-west-1.amazonaws.com/futurice-cdn/node/dist/v$NODE_VERSION/node-v$NODE_VERSION-linux-x64.tar.gz \
	&& cd /usr/local \
	&& mkdir node \
	&& cd node \
	&& tar xfz /tmp/node.tar.gz \
	&& ln -s node* current \
	&& update-alternatives --install /usr/local/bin/node node /usr/local/node/current/bin/node 5000 \
	&& update-alternatives --install /usr/local/bin/npm npm /usr/local/node/current/bin/npm 5000

# Set timezone to Europe/Helsinki
RUN echo 'Europe/Helsinki' > /etc/timezone && rm /etc/localtime && ln -s /usr/share/zoneinfo/Europe/Helsinki /etc/localtime

# Install uwsgi
RUN pip install uwsgi

# Set the locale
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

ADD requirements.txt /opt/app/

RUN useradd -m -s /bin/bash app

RUN cd /opt/app && pip install -r requirements.txt

ADD docker/supervisord.conf /etc/supervisor/supervisord.conf
ADD docker/nginx-checklist.conf /etc/nginx/conf.d/
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

COPY . /opt/app

# Set default django secret value. Required to run collectstatic.
# Real secret deployed per environment.
ENV SECRET_KEY default_insecure_secret

RUN chown -R app:app /opt/app

USER app
WORKDIR /opt/app
# Prepare assets
RUN npm install && assetgen --profile dev assetgen.yaml --force && ./manage.py collectstatic --noinput

EXPOSE 8000

# Default startup command
USER root
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]
