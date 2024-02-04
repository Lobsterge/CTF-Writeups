import requests

url = "http://chal.bearcatctf.io:48605"

r = requests.get(url+"/robots.txt")

v = r.text.replace("Allow: ", "").replace("Disallow: ","").split("\n")

useragent = b""

for i in v:
    if "User" in i:
        useragent = i[len("User-agent: "):]
        print(useragent)
        continue

    r = requests.get(url+i, headers={"User-Agent":useragent})
    if r.status_code!=418:
        print(r.text)
        input()
