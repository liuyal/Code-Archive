FROM ubuntu:latest

LABEL maintainer="jerry.liu1@se.com"

WORKDIR /home

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y vim git curl
RUN apt-get install -y python3 python3-pip libpq-dev python3-dev
RUN apt-get install -y iproute2 net-tools iputils-ping iptables
RUN apt-get install -y openssh-server openssh-client

RUN pip3 install pyasn1==0.4.8 redis==4.5.1 adaptavist atlassian-python-api jenkinsapi Typhoon-HIL-API
RUN pip3 install keyring hvac numpy dwdatareader pandas matplotlib docker psycopg2 PyGithub gitpython
RUN pip3 install pytest pytest-bdd polling tqdm xmodem psutil wmi lxml pyyaml jc Jinja2
RUN pip3 install pysnmp paramiko PyVISA pyserial flask poetry

RUN sysctl net.ipv4.conf.all.forwarding=1

RUN curl -o /usr/local/bin/fioctl -LO https://github.com/foundriesio/fioctl/releases/download/v0.38/fioctl-linux-amd64
RUN chmod +x /usr/local/bin/fioctl

RUN mkdir /var/run/sshd
RUN echo 'root:root' | chpasswd

RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]