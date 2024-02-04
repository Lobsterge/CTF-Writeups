# Proclicker V2 [web]
![challenge](challenge.png)
### Challenge:
Get your fingers ready because you will be clicking like you never have before. The old Proclick was found to have been infested with cheating hackers. Revamp your creds by winning our game the right way.
##### Links: [http://chal.bearcatctf.io:43320](http://chal.bearcatctf.io:43320)

### Solution:

We need to reach a certain score to get the flag:

```js
function showButton() {
      var goal = 5000000000;

      var score = getCookie("score");
      if((score > 1) && (score % 123982415941 == 0) && (score % 807045832 == 0) && (score % 247964831882 == 0) && (score % 201761458 == 0) && (score % 403522916 == 0) && (score % 100880729 == 0) && (score % 495929663764 == 0)) {document.getElementById("scoretitle").style.display = "block";document.getElementById("scoreredirect").style.display = "block";}else{document.getElementById("scoretitle").style.display = "none";document.getElementById("scoreredirect").style.display = "none";}
    }
```

Goal is actually bait, we just need to reach a score that is divisible by all those numbers.
I used [Z3](https://github.com/Z3Prover/z3) to find one:

```py
from z3 import *

score = Int('score')

s = Solver()

s.add(score > 1)
s.add(score % 123982415941 == 0)
s.add(score % 807045832 == 0) 
s.add(score % 247964831882 == 0) 
s.add(score % 201761458 == 0) 
s.add(score % 403522916 == 0) 
s.add(score % 100880729 == 0) 
s.add(score % 495929663764 == 0)

if s.check() == sat:
    model = s.model()
    print(model[score])
```

We can also modify our score by modifying the cookies, thus we simply need to modify our score to N-1 and click the button, giving us our flag.

Flag: ```BCCTF{cl1CKiNg_is_ju5t_Th4t_MuCH_haRd3r_94093a46}```

