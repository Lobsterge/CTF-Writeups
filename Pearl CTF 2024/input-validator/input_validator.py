target = b"oF/M5BK_U<rqxCf8zWCPC(RK,/B'v3uARD"

var3 = [1102, 1067, 1032, 1562, 1612, 1257, 1562, 1067, 1012, 902, 882, 1397, 1472, 1312, 1442, 1582, 1067, 1263, 1363, 1413, 1379, 1311, 1187, 1285, 1217, 1313, 1297, 1431, 1137, 1273, 1161, 1339, 1267, 1427]
var2 = [0 for i in range(34)]

for i in range(len(var3)):
    var3[i] -= 1337

for i in range(17):
    var2[1 + i * 2] = var3[i] //5
    var2[i * 2] =  var3[i + 17] //2

for i in range(len(var3)):
    var2[i] += target[33 - i];

for i,j in zip(var2,target):
    print(chr((i^j)%256),end="")
print()
#pearl{w0w_r3v3r51ng_15_50_Ea5y_!!}