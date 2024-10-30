from pwn import *
context.log_level = "debug"
c=[]
n=[]
s='-+*/()'
l={'-':0,'+':1,'*':1,'/':0}
# l={'-':1,'+':1,'*':0,'/':0}
j=10
def t(exp:str):
    return sum([10**i*int(exp[len(exp)-i-1],j) for i in range(len(exp))])
def calc(exp:str):
    if exp in '()': raise ValueError('Mismatched brackets')
    b=n.pop()
    a=n.pop()
    if exp=='+': n.append(a+b)
    if exp=='-': n.append(a-b)
    if exp=='/': n.append(a/b)
    if exp=='*': n.append(a*b)
def run(exp:str):
    if not exp:
        raise ValueError("Null expression")
    temp=''
    for i in exp:
        if i in s:
            if temp!='':
                n.append(t(temp))
                temp=''
            if i=='(':
                c.append(i)
            if i==')':
                while c:
                    p=c.pop()
                    if p=='(':break
                    calc(p)
                else:
                    raise ValueError("Mismatched brackets")
            if i not in '()':
                while c:
                    p=c.pop()
                    if p=='(':
                        c.append(p)
                        break
                    if l[p]>=l[i]:
                        calc(p)
                    else:
                        c.append(p)
                        break
                c.append(i)
        else:
            temp+=i
    
    if temp: n.append(t(temp))
    while c:
        calc(c.pop())
    return n[0]

r = connect("202.198.27.90", 40140)

while True:
    exp = r.recvuntil(b" = ",drop=True)
    print(exp)
    n=[]
    j = 10
    r.sendline(str(round(run(exp.decode()),2)).encode())

    success(r.recvuntil(b"u r right!\n"))