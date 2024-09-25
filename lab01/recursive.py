def r1(n):
    if n == 0:
        return 0
    return 1 + r1(n - 1)

def r2(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return n + r2(n - 2)

def r3(n):
    if n == 0:
        return 0
    return 1 + 2 * r3(n - 1)

def r4(n):
    if n == 0:
        return 0
    return 1 + r4(n - 1) + r4(n - 1)

def main():
    n = 10
    print(r1(n))
    print(r2(n))
    print(r3(n))
    print(r4(n))

if __name__ == '__main__':
    main()
