FROM ubuntu:latest

LABEL author="BUG|PWN TEAM"
LABEL desc="challenge author: RAVEN"

RUN apt update -y
RUN apt install -y socat libcurl4-openssl-dev libssh2-1 libc6-dev

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd

WORKDIR /home/ctf

COPY source .
RUN chown -R ctf:ctf /home/ctf
RUN chmod +x ./ntc

USER ctf
EXPOSE 1002

ENTRYPOINT socat TCP-LISTEN:1002,reuseaddr,fork EXEC:"stdbuf -i0 -o0 -e0 ./ntc && /bin/bash"
