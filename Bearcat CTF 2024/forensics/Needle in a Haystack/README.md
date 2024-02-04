# Needle in a Haystack [forensics]

### Challenge:
Sometimes find the flag is like finding a needle In a haystaCk, soMetimes all you need is a Push
##### Files: [needle_in_a_haystack.tar.gz](needle_in_a_haystack.tar.gz)

### Solution:
Putting together the seemingly random capitalized letters in the description we get ICMP, 
filtering by that protocol we can find an interesting packet containing this data:

```QkNDVEZ7VGhpc0lzQU5lZWRsZX0=```

Decoding from base64 gives us our flag.

Flag: ```BCCTF{ThisIsANeedle}```