from pwn import xor

flag = bytes.fromhex("982a9290d6d4bf88957586bbdcda8681de33c796c691bb9fde1a83d582c886988375838aead0e8c7dc2bc3d7cd97a4")

print(xor(flag, xor(flag, b"uoftctf{")[:8]))
#uoftctf{x0r_iz_r3v3rs1bl3_w17h_kn0wn_p141n73x7}