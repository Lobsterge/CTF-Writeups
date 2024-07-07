from pwn import *

with open("text.data", "rb") as f: #.data section
    data = b"".join(f.readlines())

data = data[16:] #removing __data_start and __dso_handle

canary = {}

for i in range(0, len(data), 8): #mapping each number to its corrisponding canary
    canary[i//8]=data[i:i+8]
print(hex(u64(canary[14927])))
exit()    

with open("lost_canary_dbg.c", "r") as f: #parsing the decompiled functions
    data = (("".join(f.readlines())).split("void station"))[1:]

for idx, i in enumerate(data):
    if "fgets" in i:
        if b"\x00" in canary[idx]:
            continue
    elif "gets" in i:
        if b"\n" in canary[idx]:
            continue
    elif "scanf" in i:
        if b" " in canary[idx]:
            continue
    print(f"FOUND {idx}")