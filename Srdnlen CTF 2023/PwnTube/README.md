# PwnTube
![challenge](challenge.png)
### Challenge:
##### Who is this guy? And why can't I skip this ad?! He really looks like someone who could never give me up though :)
##### This is a remote challenge, you can connect to the service with: nc pwntube.challs.srdnlen.it 1661
##### Author: manu_massi

##### Files: [PwnTube](PwnTube)

### Solution:

This binary has 2 main vulnerabilities, a buffer overflow in the buy_premium() function and a format string when adding comments.

I firstly leaked the stack canary and the pie using the format string, i then tried to jump to one of the many ```system("cat ./flag")``` in the binary, sadly those were just bait so we need to pop a shell.

I leaked aslr by using this payload:

```py
payload = b"A"*504 + p64(canary)*2 + POP_RDI + p64(elf.got["puts"]) +p64(elf.plt["puts"]) + RET*2 + p64(elf.sym["main"])
```

Which gives us our libc leak, which we can use to get our  ```"/bin/sh"``` string, now that we have all we need we can do a simple rop-chain to call ```system("/bin/sh")``` and get our flag:

Flag: ```srdnlen{pwn4t1n4?}```