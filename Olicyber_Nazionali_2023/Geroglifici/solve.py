from pwn import *

r=remote("geroglifici.challs.olicyber.it", 35000)

r.recvline()
r.recvline()
r.recvline()

ct=r.recvline()[20:-1]

alpha="abcdefghijklmnopqrstuvwxyz0123456789{}_ABCDEFGHIJKLMNOPQRSTUVWXYZ"

r.sendline(alpha.encode())

data=r.recvline()
data=str(r.recvline()[2:-1])[2:-1]

count=0
memo={}

for i in range(0, len(data), 16):
    key=""
    for j in range(0, 16):
        key+=data[i+j]
    memo[key]=alpha[count]
    count+=1

ct=str(ct)[2:-1]
for i in range(0, len(ct), 16):
    key=""
    for j in range(0, 16):
        key+=ct[i+j]
   
    print(memo[key], end="")




