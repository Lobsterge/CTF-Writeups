''' L = goal, S = sands, u start at [0;0]

.###.....#
..#S.##..#
#.S#.#SS.#
#..#.#..##
.S.#.#.SS.
.###.#.S..
...#.#...S
##.#.####.
.S.S.#..S.
..S..#LS..

'''

from pwn import *

elf = context.binary = ELF("sands")
#r = process()
r = remote("chal.nbctf.com", 30401)

'''gdb.attach(r, gdbscript="""
    break *0x401b1a"""+
    """\nfinish"""*3+
    """\nc"""*40)'''

moves = b"sdssssaassddssddwwwwwwwwwwdddsssssssddssssaaaaaaa"

r.sendline(moves)
r.interactive()