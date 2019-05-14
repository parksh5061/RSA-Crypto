import random

def rsa_genkey(key_length):
    e = 2
    pk =  []
    sk = []

    key_length = int(key_length/2) # key_length가 1024비트 일경우 p,q를 각각 512비트로 구해준다.

    while(1):
        p = random.randint(pow(2,key_length), pow(2,key_length+1)-1) # p를 범위 내에 랜덤한 정수를
        if(is_prime(p) == 1):
           break;

    while(1):
        q = random.randint(pow(2,key_length), pow(2,key_length+1)-1)
        if(p == q):
            continue;
        if (is_prime(q) == 1):
            break;

    n = p*q
    oiler_n = (p-1)*(q-1)

    while(1):
        if(gcd(e,oiler_n) == 1):
            break;
        else:
            e = e + 1

    d = extended_gcd(e,oiler_n)

    while (1):
        if (d < 0):
            d = d + oiler_n
        elif (d > 0):
            break;

    pk.append(n)
    pk.append(e)

    sk.append(p)
    sk.append(q)
    sk.append(d)

    return pk,sk

def rsa_encrypt(m,pk):
    c = mod_exp(m,pk[1],pk[0])

    return c

def rsa_decrypt(ct,sk):
    m = mod_exp(ct,sk[2],sk[0]*sk[1])

    return m

# 유클리드 호제법으로 최대공약수를 구하는 gcd 함수
def gcd(a, b):
    if b > a: # 만약 b가 a보다 클 경우 a와 b를 바꿔주는 조건문
        temp = b
        b = a
        a = temp

    modular = -1 # 아래 while문을 실행시키기 위해 임의로 modular 값을 설정해두었음
    while modular != 0:
        modular = int(a % b) # modular는 a와 b의 나머지를 저장시킴
        if modular == 0: # 만약 modular가 0이면 break 시킴
            break

        a = b # modular가 0이 아니면 a에 b를 저장시킴
        b = modular # b에는 modular 값을 저장시킴

    return b # b의 값을 반환시킴

def miller_rabin_test(n,b,s,t):
    base = []
    i=0

    base.append(mod_exp(b,t,n))

    while(i != s):
        if(i == 0):
            if(base[i] % n == 1 or base[i] % n == (n-1)):
                return 1
            else :
                base.append(pow(base[i], 2))
                i = i + 1
        else:
            if(base[i] % n == 1) :
                return 0
            elif(base[i] % n == (n-1)):
                return 1
            else:
                base.append(pow(base[i],2))
                i = i + 1
    if(base[i] % n != (n-1)):
        return 0
    else:
        return 1


def is_prime(n):
    cnt = 0
    i = 1

    if(n % 2 == 0):
        return 0

    while(1):
        save = (n-1) // pow(2,i)

        if(n == 2):
            k=i
            t = save
            break;

        if(save != 0):
            k = i
            t = save
            break;
        i = i + 1

    for i in range(0,20):
        b = random.randint(1, n - 1)

        if(b % 2 == 0):
            b = b + 1

        result = miller_rabin_test(n, b, k, t)
        if(result == 1):
            cnt = cnt + 1
        else:
            return 0
        if(cnt == 20):
            return 1

def mod_exp(a,e,n):
    arr = []
    r = []
    s = []
    save = e
    cnt=0
    j=1
    result=1

    # e의 바이너리 값을 구하는 부분
    while save!=0: # save가 0이 아닐때까지 반복 시켜줌
        arr.append(save%2) # arr 배열에 save 값을 2로 나눈 나머지를 추가시켜줌
        save = save//2 # save에 save//2 값을 저장시킴
        cnt = cnt + 1 # 횟수를 저장하기 위한 cnt 값 1 증가

    # e의 바이너리 값에 대한 2진값을 구하는 부분
    for i in range (0,cnt): # i를 0~cnt까지 반복시킴
        if arr[i] == 1 : # 만약 바이너리값이 1이면 r배열에 j를 저장시켜줌
            r.append(j)
        j = j * 2 # 2진값이므로 다음 값은 2를 곱한 값이므로 j에 2를 곱해줌

    # 함수의 나머지를 구하는 부분
    for i in range(0,cnt): # i를 0~cnt까지 반복시킴
        if(i==0): # 만약 i가 0이면 a % n해줌
            s.append(a % n)
        else: # 만약 i가 1이 아니면 s[i-1] * s[i-1] % n 해줌
            s.append(s[i-1] * s[i-1] % n)

        if(arr[i] == 1): # 만약 arr[i]가 1이면
            result = result * s[i] # result에 s[i]를 곱해줌

    result = result % n # result 값에 mod n을 해주면 바이너리 값을 이용한 나머지 값을 구할 수 있음

    return result;

#확장된 유클리드 호제법으로 최대공약수를 구하는 extended_gcd2 함수
def extended_gcd(a, b):
    button = 0 # b가 a보다 클 경우 리턴 값을 달리해주기 위해서 boolean 역할을 하는 button 변수 생성
    if b > a: # b가 a보다 클 경우 두 개의 값을 바꿔주고 button을 1로 바꿔줌
        temp = b
        b = a
        a = temp
        button = 1

    modular = -1 # while문을 돌리기 위해 임의로 값을 넣어주었음
    i = 2 # 배열의 원소를 관리해주기 위한 i 값
    cnt = 0 # 몇번 실행하였는지 확인하기 위한 cnt 값
    x = [1, 0] # 확장된 유클리드 호제법이 초기에 x 값이 1, 0이므로 배열에 1,0으로 초기화 시켜주었음
    y = [0, 1] # 확장된 유클리드 호제법이 초기에 y 값이 0, 1이므로 배열에 0,1으로 초기화 시켜주었음

    while modular != 0:
        modular = int(a % b) # modular 값을 a % b 값으로 저장시켜주었음
        if modular == 0: # modular가 0일 경우 break 시켜서 나감
            break
        divide = int(a // b) # divide에 a / b 의 값을 저장 시킴

        x.append(1) # x에 다음 원소 값이 존재해야 아래에서 x[i] 값을 저장시킬 수 있으므로 임의로 1을 집어넣어주었음
        y.append(1) # 위와 동일

        x[i] = x[i-2] - divide * x[i-1] # x 값을 저장시키기 위한 공식
        y[i] = y[i-2] - divide * y[i-1] # y 값을 저장시키기 위한 공식

        cnt = cnt + 1 # cnt 값 1 증가
        i = i + 1 # i 값 1 증가
        a = b # a에 b를 저장시킴
        b = modular # b에 modular를 저장시킴
    if button == 0: # 만약 button이 0이면
        return x[cnt+1] # b와 (x,y)로 리턴해줌
    return y[cnt+1] # button이 1이면 b와 (y,x)로 리턴해줌

pk=[]
sk=[]

key_length = int(input())
pk,sk = rsa_genkey(key_length)
m = 1234
ct = rsa_encrypt(m,pk)
m2 = rsa_decrypt(ct,sk)
print("m2",m2)


