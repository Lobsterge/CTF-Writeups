from pwn import *
from string import printable

r = remote("babycha.chal.irisc.tf", 10100)

r.sendline(b"1")
r.sendline(b"A"*16)
r.sendline(b"2")
r.recvuntil(b"> ")
r.recvuntil(b"> ")
target=r.recvline()[:-1]

flag_1 = b"irisctf{initiali"
flag_2 = b"zation_is_no_pro"
flag_3= b""

#irisctf{initialization_is_no_problem}

while True:
    print(flag_1+flag_2+flag_3)
    
    if b"}" in flag_3:
        input()

    for i in printable:
        r = remote("babycha.chal.irisc.tf", 10100)
        r.sendline(b"1")
        r.sendline(b"A"*16)
        r.recvuntil(b"> ? ")
        r.sendline(b"1")
        r.sendline(flag_1 + flag_2 + flag_3 + i.encode())
        r.recvuntil(b"> ? ")
        answer=r.recvline()[:-1]
        print(answer[64:])
        print(target[64:64+len(answer[64:])])
        if answer[64:] == target[64:64+len(answer[64:])]:
            flag_3+=i.encode()
            break


'''for i in range(100):

    tmp1 =0

    for _ in range(2):

        r = remote("babycha.chal.irisc.tf", 10100)

        r.sendline(b"1")
        r.sendline(b"A"*16)
        r.sendline(b"2")
        r.recvuntil(b"> ")
        r.recvuntil(b"> ")
        d=r.recvline()[:-1]

        #d6fd52a3f94c25cf654d4722bc0b1020c0f739f943b95286a20b9d47d422ad19626c656d7d

        #0b0d5daa6f0c9472dad5a21152968830095fbf163a352bc3f79eadc05ac496d0626c656d7d

        print(d)
        print(d)

        if tmp1==d[64:64+16]:
            print(i*8)
            input()
        tmp1=d[64:64+16]'''
