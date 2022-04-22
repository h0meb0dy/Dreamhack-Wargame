FROM ubuntu:18.04

ENV user iofile_aaw
ENV chall_port 7182

RUN apt-get update
RUN apt-get -y install socat

RUN adduser $user

ADD ./flag /home/$user/flag
ADD ./$user /home/$user/$user
ADD ./libc.so.6 /home/$user/libc.so.6
ADD ./run.sh /home/$user/run.sh

RUN chown -R root:root /home/$user
RUN chown root:$user /home/$user/flag
RUN chown root:$user /home/$user/$user

RUN chmod 755 /home/$user/run.sh
RUN chmod 755 /home/$user/$user
RUN chmod 440 /home/$user/flag


WORKDIR /home/$user
USER $user
EXPOSE $chall_port
CMD socat -T 10 TCP-LISTEN:$chall_port,reuseaddr,fork EXEC:/home/$user/run.sh








