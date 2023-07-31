from pwn import *
import ctypes
from time import time

host = "challs.tfcctf.com"
port = 30421
libc = ctypes.CDLL('/lib/x86_64-linux-gnu/libm.so.6')

r=remote(host,port)
libc.srand(int(time()))

for i in range(10):
    num=libc.rand()
    r.sendline(str(num).encode())
r.interactive() 