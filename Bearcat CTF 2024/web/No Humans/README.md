# No Humans [web]

### Challenge:
My robot is making secret plans. Unfortunately I was given strict plans not to show up. Find out what they are planning.
##### Links: [http://chal.bearcatctf.io:48605/](http://chal.bearcatctf.io:48605/)

### Solution:

There are a bunch of links in the /robots.txt file, most likely the flag is hidden in one of them.
We can make a simple crawler to check if one of those pages contains the flag.

I was also changing my user-agent for the requests but im not sure it was needed.

Solve script: [solve.py](solve.py)

Flag: ```BCCTF{Th1s_Is_wHy_Hum4ns_N33d_4ppLy}```