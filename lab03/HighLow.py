import random

total_attempts = []
attempts = 0

def median(lst):
    n = len(lst)
    s = sorted(lst)
    return (sum(s[n//2-1:n//2+1])/2.0, s[n//2])[n % 2] if n else None

def HighLow(Number, low, max):
    global attempts
    attempts += 1

    guess = (low + max) // 2
    if guess == Number:
        return
    elif guess > Number:
        max = guess - 1
        HighLow(Number,low,max)
    else:
        low = guess + 1
        HighLow(Number,low,max)

def main():
    wanted_attempts = 10000
    for i in range(wanted_attempts):
        global attempts
        attempts = 0
        low = 1
        max1 = 100
        Number = random.randint(low,max1)
        HighLow(Number,low,max1)
        total_attempts.append(attempts)
    
    #results
    for i in range(max1):
        count = total_attempts.count(i+1)
        if count > 0:
            print("Number of attempts: ", i+1, "Count: ", count, "Percentage: ", round(count/max1,2), "%")
            
    print ("Average attempts (MEAN): ", sum(total_attempts)/wanted_attempts)
    print ("Median attempts: ", int(median(total_attempts)))
    print("Min attempts: ", min(total_attempts))
    print("Max attempts: ", max(total_attempts))

if __name__ == "__main__":
    main()

        

