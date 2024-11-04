#a^b = a * a ^ (b-1)

brute_force_calls = 0
divide_and_conquer_calls = 0
decrease_and_conquer_calls_recursive= 0
decrease_and_conquer_calls_iterative = 0

def brute_force_recursive(a, b):
    global brute_force_calls
    brute_force_calls += 1
    
    if b == 0:
        return 1
    return a * brute_force_recursive(a, b-1)

def divide_and_conquer_recursive(a, b):
    global divide_and_conquer_calls
    divide_and_conquer_calls += 1
    
    if b == 0:
        return 1
    if b == 1:
        return a
    
    half1 = divide_and_conquer_recursive(a, b // 2)
    half2 = divide_and_conquer_recursive(a, (b + 1) // 2)
    
    return half1 * half2

def decrease_and_conquer_recursive(a, b):
    global decrease_and_conquer_calls
    decrease_and_conquer_calls += 1
    
    if b == 0:
        return 1
    if b == 1:
        return a
    
    # Calculate a^(b//2) once and store it
    half_result = decrease_and_conquer_recursive(a, b // 2)
    
    # If b is even: a^b = (a^(b//2))^2
    if b % 2 == 0:
        return half_result * half_result
    # If b is odd: a^b = a * (a^((b-1)//2))^2
    else:
        return a * half_result * half_result
    
def decrease_and_conquer_iterative(a, b):
    global decrease_and_conquer_calls_iterative
    decrease_and_conquer_calls_iterative += 1
    result = 1
    for i in range(b):
        result *= a
    return result
    

def main():
    global brute_force_calls, divide_and_conquer_calls, decrease_and_conquer_calls
    a = 2
    b = 11
    
    brute_force_calls = 0
    divide_and_conquer_calls = 0
    decrease_and_conquer_calls = 0
    
    brute_result = brute_force_recursive(a, b)
    print(f"Brute Force Result: {brute_result}, Calls: {brute_force_calls}")
    
    divide_result = divide_and_conquer_recursive(a, b)
    print(f"Divide and Conquer Result: {divide_result}, Calls: {divide_and_conquer_calls}") 

    decrease_result = decrease_and_conquer_recursive(a, b)
    print(f"Decrease and Conquer Result: {decrease_result}, Calls: {decrease_and_conquer_calls}")

    decrease_iterative_result = decrease_and_conquer_iterative(a, b)
    print(f"Decrease and Conquer Iterative Result: {decrease_iterative_result}, Calls: {decrease_and_conquer_calls_iterative}")

if __name__ == "__main__":
    main()
