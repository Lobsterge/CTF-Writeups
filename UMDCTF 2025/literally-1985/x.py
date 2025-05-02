from pwn import *

r = remote("challs.umdctf.io", 31085)

with open("x.js", "r") as f:
    v = f.read()+"\nEOF"

r.sendline(v.encode())
r.interactive()
    