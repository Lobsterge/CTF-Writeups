import requests

url="http://chal.bearcatctf.io:43806/check_number"

r = requests.post(url, params={"number":0x55c88be0})

print(r.text)
#BCCTF{Wh4t_k1nD_0F_m4tH_I5_tH4T?!?_8053c548}