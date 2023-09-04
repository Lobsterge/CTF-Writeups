import requests
import pytesseract 
from PIL import Image
from base64 import b64decode


url = "https://captcha1.uctf.ir/"
s=requests.session()

r=s.get(url)

data=str(r.text)


for _ in range(1000000):
    print(_)
    image=""
    count=0
    for i in data:
        if count==3:
            if i=='"':
                break
            image+=i
        if i==",":
            count+=1
    file=open("temp.png", "wb")
    file.write(b64decode(image))
    file.close()
    
    image = Image.open("temp.png")
    ans = pytesseract.image_to_string(image).rstrip()
    data=s.post(url, data={"captcha":ans})
    data=str(data.text)
    
    if _ > 285 or _%5==0:
        print(data)


