from pwn import *
from Crypto.Util.number import long_to_bytes, bytes_to_long

r = remote("chal.bearcatctf.io", 36242)

r.recvuntil(b"Ciphertext of Flag: ")
ct=int(r.recvline()[:-1])

r.sendline(b"KEY:")
N=int(r.recvline()[2:-1])
r.recvline()
r.recvline()

r.sendline(f"DECRYPT:{ct+N}".encode())
dec=int(r.recvline()[:-1])
print(long_to_bytes(dec).decode())
#BCCTF{Th3_0rACl3_OlIv1a_iS_Never_wR0nG}