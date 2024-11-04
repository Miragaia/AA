import time

num_adds = 0 
start = time.time()

def Fibonacci(n):
    start = time.time()
    global num_adds
    if (n <= 1):
        return n
    
    num_adds += 1

    return Fibonacci(n-1) + Fibonacci(n-2)

def main():
    for i in range(0, 30):
        global num_adds
        num_adds = 0
        print("Fibonacci of", i, "is", Fibonacci(i), "and took", num_adds, "additions", "and", time.time() - start, "seconds")

if __name__ == "__main__":
    main()

    