from pwn import *

r = remote("babyrevjohnson.chal.irisc.tf", 10002)

color = ["dummy", "red", "blue", "green", "yellow"]
food = ["dummy", "pizza", "pasta", "steak", "chicken"]

r.sendline(color[1])
r.sendline(color[4])
r.sendline(color[3])
r.sendline(color[2])

r.sendline(food[4])
r.sendline(food[2])
r.sendline(food[3])
r.sendline(food[1])

#irisctf{m0r3_th4n_0n3_l0g1c_puzzl3_h3r3}
r.interactive()