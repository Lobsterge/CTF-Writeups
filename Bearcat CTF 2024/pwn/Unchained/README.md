# Unchained [pwn]
![challenge](challenge.png)
### Challenge:
Unchain yourself from your tables.
##### Links: ```nc chal.bearcatctf.io 42401```
##### Files: [challenge.zip](challenge.zip)

### Solution:

We have a 4 byte arbitrary read/write as we can chose an arbitrary index, we can use it to read an address from the got
thus leaking ASLR, then we can simply overwrite the got of the exit function with a onegadget.

Solve script: [solve.py](solve.py)

Flag: ```BCCTF{L1b_C_3xp3rt_7d1665c6}```