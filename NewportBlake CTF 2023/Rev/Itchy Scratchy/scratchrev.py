alpha = ["@", "z","v","t","w","r","c","a","5","7","n","4","9","u","2","b","y","1","j","d","q","o","6","g","0","k","s","x","f","i","8","p","e","l","m","h","3"]
enc = [-1, 902,764,141,454,207,51,532,1013,496,181,562,342]
name = [-1, 29, 26, 7, 7, 6, 0, 10, 32, 4, 3, 21, 10]
input = []
alpha2 = {}

for o, i in enumerate(alpha):
    alpha2[i]=o

flag = "nbctf{12lett3rf149}"
answer = "@12lett3rf149"

for i in answer:
    input.append(alpha2[i])

j = 1

''' correct inputs
input[1] = 17
input[2] = 14
input[3] = 33
input[4] = 32
input[5] = 3
input[6] = 3
input[7] = 36
input[8] = 5
input[9] = 28
input[10] = 17
input[11] = 11
input[12] = 12'''


k=1
while k<=12:
    i=1
    j=1
    while i<=12:
        j = (i*i+name[i])%12+1
       
        #enc[i] -= name[i]*name[j]
        tmp = input[i]*input[j] + name[i]*name[j]

        if tmp != enc[i]:
            exit(0)

        i+=1
    break

print("ok")
       
''' i j pairs
1 7
2 7
3 5
4 12
5 8
6 1
7 12
8 1
9 2
10 8
11 11
12 11'''