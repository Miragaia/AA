import time

def delannoyV1(m, n):
    if m == 0 or n == 0:
        return 1
    
    return delannoyV1(m - 1, n) + delannoyV1(m - 1, n - 1) + delannoyV1(m, n - 1)

# Test cases
print(f"V1-D(1,1) = {delannoyV1(1, 1)}")
print(f"V1-D(2,2) = {delannoyV1(2, 2)}")
print(f"V1-D(2,3) = {delannoyV1(2, 3)}")
start = time.time()
print(f"V1-D(12,12) = {delannoyV1(14, 14)}")
finish = time.time()
print(f"Time: {finish - start}")

print("\n")

def delannoyV2(m, n):
    D = [[0 for _ in range(n+1)] for _ in range(m+1)]
    
    for i in range(m+1):
        D[i][0] = 1
    for j in range(n+1):
        D[0][j] = 1
    
    for i in range(1, m+1):
        for j in range(1, n+1):
            D[i][j] = D[i-1][j] + D[i-1][j-1] + D[i][j-1]
    
    return D[m][n]

# Test cases
print(f"V2-D(1,1) = {delannoyV2(1, 1)}")
print(f"V2-D(2,2) = {delannoyV2(2, 2)}")
print(f"V2-D(2,3) = {delannoyV2(2, 3)}")
print(f"V2-D(3,2) = {delannoyV2(3, 2)}")
