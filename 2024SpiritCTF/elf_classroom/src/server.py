import random
import time

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

OPERATORS = ['+', '-', '*', '/']
def get_random_operator():
    return random.choice(OPERATORS)

def get_random_operand():
    return str(random.randint(1, 9))

def generate_prefix_expression(n):
    if n == 1:
        return get_random_operand()
    
    operator = get_random_operator()
    left_expr = generate_prefix_expression(n - 1)
    right_operand = get_random_operand()
    
    return f'{operator} {left_expr} {right_operand}'

def prefix_to_infix(prefix_expr):
    stack = []
    tokens = prefix_expr.split()[::-1]  # 倒序处理
    for token in tokens:
        if token.isdigit():
            stack.append(token)
        else:
            operand1 = stack.pop()
            operand2 = stack.pop()
            stack.append(f'({operand1} {token} {operand2})')
    return stack[-1]

def generate_expressions(n):
    return prefix_to_infix(generate_prefix_expression(n)).replace(" ", "").replace("(","").replace(")","")

for i in range(100):
    c=[]
    n=[]
    j=10
    # exp='10+2*3-(5*2)+2*6+6'
    exp = generate_expressions((i+1)*5)
    start = time.time()
    print(exp, end=" = ")
    ss = input()
    end = time.time()
    if end - start > 2:
        print("Too slow! zako~")
        exit(0)
    ans = round(run(exp),2)
    try:
        assert ans == float(ss)
    except ValueError:
        print("wrong data!")
        exit(0)
    except AssertionError:
        print("ba~ka~, here's a hint 4 u!")
        print("the ans of {} is {}!".format(exp, ans))
        exit(0)
    finally:
        print("u r right!")
print("Give u flag: ")
print(open("/flag").read())