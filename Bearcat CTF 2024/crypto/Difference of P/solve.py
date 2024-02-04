from Crypto.Util.number import inverse, long_to_bytes

#script taken from https://ctftime.org/writeup/21690

#--------data--------#

c=1974980851853019257771773253811679794137241209581612326758022524735213521549252839752456399226743 
N=22124683985039812698470600343255891405990431861180855450772516395200335369863431601013187704080051 
e = 65537


#--------helper functions--------#

def isqrt(n):
  x = n
  y = (x + n // x) // 2
  while y < x:
    x = y
    y = (x + n // x) // 2
  return x

# fermat factorization
def fermat(n, verbose=False):
    a = isqrt(n) # int(ceil(n**0.5))
    b2 = a*a - n
    b = isqrt(n) # int(b2**0.5)
    count = 0
    while b*b != b2:
        if verbose:
            print('Trying: a=%s b2=%s b=%s' % (a, b2, b))
        a = a + 1
        b2 = a*a - n
        b = isqrt(b2) # int(b2**0.5)
        count += 1
    p=a+b
    q=a-b
    assert n == p * q
    return p, q

#--------rsa--------#

p, q = fermat(N)
phi = (p - 1) * (q - 1)
d = inverse(e, phi)
m = pow(c, d, N)
flag = long_to_bytes(m).decode()

print(flag)
#BCCTF{F3rMaT_yOu_BugG3r}
#https://ctftime.org/writeup/21690



