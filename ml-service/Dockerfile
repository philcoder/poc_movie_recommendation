FROM debian:stretch

LABEL maintainer="Philipp B. Costa"

ENV PATH /usr/local/bin:$PATH

ENV LANG C.UTF-8

#use br repositories for speedup network
RUN echo 'deb http://ftp.br.debian.org/debian stretch main' > /etc/apt/sources.list
RUN echo 'deb http://security.debian.org/debian-security stretch/updates main' >> /etc/apt/sources.list
RUN echo 'deb http://ftp.br.debian.org/debian stretch-updates main' >> /etc/apt/sources.list

RUN apt-get update && apt-get install -y --no-install-recommends \
		ca-certificates \
		libexpat1 \
		libffi6 \
		libgdbm3 \
		libreadline7 \
		libsqlite3-0 \
		libssl1.1 \
		psmisc \
		nano \
		procps \
	&& rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install pika psycopg2-binary

WORKDIR /home/service