import requests

url = "https://captcha2.uctf.ir/"

match={
    "6D0EBBBDCE32474DB8141D23D2C01BD9628D6E5F.jpeg":"rabbit",
    "73335C221018B95C013FF3F074BD9E8550E8D48E.jpeg":"penguin",
    "9E05E6832CAFFCA519722B608570B8FF4935B94D.jpeg":"mouse",
    "148627088915C721CCEBB4C611B859031037E6AD.jpeg":"snake",
    "9D989E8D27DC9E0EC3389FC855F142C3D40F0C50.jpeg":"cat",
    "5ECE240085B9AD85B64896082E3761C54EF581DE.jpeg":"duck",
    "E49512524F47B4138D850C9D9D85972927281DA0.jpeg":"dog",
    "FF0F0A8B656F0B44C26933ACD2E367B6C1211290.jpeg":"fox",
    "C29E4D9C8824409119EAA8BA182051B89121E663.jpeg":"hawk",
    "09F5EDEB4F5B2A4E4364F6B654682C6758A3FA16.jpeg":"bear",
    "091B5035885C00170FEC9ECF24224933E3DE3FCC.jpeg":"horse"
}

def parse(text):
    tmp1=""
    tmp2=""
    pos=text.find("src")+5
    for i in range(100):
        if text[pos+i]=='"':
            break
        tmp1+=text[pos+i]
    pos=text.find("src", pos)+5
    for i in range(100):
        if text[pos+i]=='"':
            break
        tmp2+=text[pos+i]
    return (tmp1, tmp2)


s=requests.session()

r=s.get(url)

data=str(r.text)


for _ in range(1000):

    tmp1, tmp2 = parse(data)
    
    print(_)
  
    ans=match[tmp1]+"-"+match[tmp2]
    data=s.post(url, data={"captcha":ans})
    data=str(data.text)
    
    if _ > 90 or _%5==0:
        print(data)
   


