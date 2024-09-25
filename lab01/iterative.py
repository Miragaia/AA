def f1(n):
    r = 0
    for i in range(1, n + 1):
        r += i
    return r

def f2(n):
    r = 0
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            r += 1
    return r

def f3(n):
    r = 0
    for i in range(1, n + 1):
        for j in range(i, n + 1):
            r += 1
    return r

def f4(n):
    r = 0
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            r += j
    return r

def main():
    n = 10
    print(f1(n))
    print(f2(n))
    print(f3(n))
    print(f4(n))

if __name__ == '__main__':
    main()