FROM gcc:13.2.0

ARG FLAG

EXPOSE 1337

RUN apt update && apt install -y socat

RUN mkdir /app
WORKDIR /app

RUN useradd pwn -d /app

RUN echo $FLAG > /flag

COPY Makefile .
COPY brainfrick.cpp .

RUN make

USER pwn

CMD ["socat", "TCP4-LISTEN:1337,reuseaddr,fork", "EXEC:./brainfrick"]
