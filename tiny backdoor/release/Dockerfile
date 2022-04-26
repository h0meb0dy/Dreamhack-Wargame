FROM ubuntu:18.04

RUN sed -i -re 's/([a-z]{2}.)?archive.ubuntu.com|security.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list && \
    apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y socat

RUN adduser --no-create-home --disabled-login --gecos '' -- "backdoor" && mkdir -p "/home/backdoor"

COPY --chown=backdoor:backdoor ./deploy/backdoor /home/backdoor/
COPY --chown=backdoor:backdoor ./deploy/flag.txt /home/backdoor/

RUN chmod 750 "/home/backdoor/backdoor" && chmod 750 "/home/backdoor/flag.txt"

ENV LANG C.UTF-8
ENV TERM linux

WORKDIR /home/backdoor
EXPOSE 7777/tcp
CMD ["socat", "TCP-LISTEN:7777,reuseaddr,fork", "EXEC:/home/backdoor/backdoor,nofork,stderr,setsid,su=backdoor"]
