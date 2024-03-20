from pwn import *

with open("flag.txt.enc", "rb") as f:
    v=f.readline()
    print(v)

def ROR(x, n):
    mask = (2**n) - 1
    mask_bits = x & mask
    return (x >> n) | (mask_bits << (32 - n))

for i in range(0, len(v), 4):
    tmp1 = u32(v[i:i+4])
    print(p32(ROR(tmp1, 0xd)).decode(),end="")
print()
#wctf{i_th1nk_y0u_m1sund3rst00d_h0w_r0t13_w0rk5}