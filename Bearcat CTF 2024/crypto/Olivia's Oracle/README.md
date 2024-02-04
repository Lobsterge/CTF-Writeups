# Olivia's Oracle [crypto]

### Challenge:
Olivia made a third party oracle for messages sent to other parties. It handles encryption and decryption, to make sure you can trust it, it even sends you the flag to show you can't decrypt it.
##### Links: ```nc chal.bearcatctf.io 36242```
##### Files: [Olivias_Oracle.zip](Olivias_Oracle.zip)

### Solution:
We can encrypt and decrypt everything we want, the modulus and the ciphertext of the flag are also given to us.
However we cant simply decrypt the ciphertext as the server will refuse to decrypt that particular ciphertext.
We thus need to find a way to maintain the plaintext while having a different ciphertext, we can achieve that by simply adding N to the ciphertext.

Solve script: [solve.py](solve.py)

Flag: ```BCCTF{Th3_0rACl3_OlIv1a_iS_Never_wR0nG}```