from pwn import *

def solve(n,k,stairs):

    pos = 0
    ans = 0

    while pos!=n-1:
        if pos+k>n:
            return ans+1

        if stairs[pos+k]=='0':
            pos+=k
        else:
            j = 1
            while stairs[pos+k-j]!='0':
                j+=1
                if pos+k-j<=pos:
                    return -1
            pos+=k-j
        ans+=1
    
    return ans

r = remote("chal.nbctf.com", 30270)

t = int(r.recvline()[:-1].decode())

for _ in range(t):
    print(_)
    data = r.recvline()[:-1].decode().split(" ")
    n = int(data[0])
    k = int(data[1])
    stairs = r.recvline()[:-1].decode()

    ans = solve(n,k,stairs)

    r.sendline(str(ans).encode())

r.interactive()   