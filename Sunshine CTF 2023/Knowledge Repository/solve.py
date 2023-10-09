memo={}

def add(number, letter):
    with open("output/data"+str(number), "rb") as f:
        tmp1=f.read()
    memo[tmp1]=letter

add(0, "=")
add(5, "A")
add(6, "4")
add(7, "B")
add(8, "O")
add(9, "C")
add(10, "Q")
add(11, "V")
add(12, "P")
add(14, "W")
add(15, "I")
add(16, "X")
add(18, "7")
add(20, "G")
add(21, "H")
add(22, "J")
add(25, "M")
add(27, "L")
add(28, "2")
add(29, "D")
add(31, "S")
add(39, "R")
add(40, "N")
add(43, "Z")
add(44, "E")
add(51, "6")
add(53, "T")
add(55, "U")
add(59, "F")
add(72, "5")
add(74, "3")
add(79, "K") 
add(2990, "Y")

kk=open("result.txt", "a")
for i in range(3015, -1, -1):
    with open("output/data"+str(i), "rb") as f:
        tmp1=f.read()
    if tmp1 in memo.keys():
        kk.write(memo[tmp1])
        continue
    print("unknown at "+str(i))
    break
kk.close()