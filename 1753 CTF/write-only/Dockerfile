FROM debian:bookworm-20240211

ARG FLAG

EXPOSE 1337

RUN apt update && apt install -y socat

RUN mkdir /app
WORKDIR /app

RUN useradd pwn -d /app

RUN echo $FLAG > flag

COPY writeonly .

USER pwn

CMD ["socat", "TCP4-LISTEN:1337,reuseaddr,fork", "EXEC:./writeonly"]
