#how many ways to move in steps of 1 or 2 or 3 meters
def moveRecursive(n):
    if n == 0:
        return 1
    if n < 0:
        return 0
    return moveRecursive(n-1) + moveRecursive(n-2) + moveRecursive(n-3)

def moveArray(n):
    pass
    

def main():
    meters= 10
    print("Number of ways to move", meters, "meters in Recursive")
    for i in range(0, meters):
        print("Number of ways to move", i+1, "meters is", moveRecursive(i+1))

if __name__ == "__main__":
    main()
    