# WASMs REvenge [rev]

### Challenge:
So you thought you could escape RE by running to Web?
##### Links: [http://chal.bearcatctf.io:43806](http://chal.bearcatctf.io:43806)

### Solution:
The website will asks us for a number, if we input the correct one we will get our flag.
The number is checked using a wasm program, we can get download it by simply going to [http://chal.bearcatctf.io:43806/static/REading.wasm](http://chal.bearcatctf.io:43806/static/REading.wasm).

This is the decompiled wasm code:

```c
undefined4 export::big_math_things(int param1)
{
  if (((((param1 + 0x467) / -0x236) * -5 + -0xe7550) * 0x18) / 0x56e5 != -0x5b) {
    return 0;
  }
  return 0x55c88be0;
}
```

So we simply need to make the function return 0x55c88be0.

However we dont actually need to bother as we can send the number ourselves:

```py
import requests

url="http://chal.bearcatctf.io:43806/check_number"

r = requests.post(url, params={"number":1439206368})

print(r.text)
#BCCTF{Wh4t_k1nD_0F_m4tH_I5_tH4T?!?_8053c548}
```


Flag: ```BCCTF{Wh4t_k1nD_0F_m4tH_I5_tH4T?!?_8053c548}```