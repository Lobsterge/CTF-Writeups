rune=0

with open("the", "r") as f:
    rune = f.readline()

z=0
for i in rune:
    print(chr((ord(i)-z)%256),end="")
    z=(ord(i)-z)%256

print()
#irisctf{i_r3411y_1ik3_num63r5}