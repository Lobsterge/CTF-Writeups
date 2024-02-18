from pwn import *

r = remote("chall.lac.tf", 31321)

payload = b"pretty"*15+b"please"*39+b"flag"

r.sendline(payload)
r.interactive()
#lactf{next_year_i'll_make_aplet456_hqp3c1a7bip5bmnc}