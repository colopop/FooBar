def answer(n):
    
    n = long(n) 
    
    count = 0
    while n > 0:
        if n == 1: # this is out goal. if we're here, we can stop
            break
        if n == 3: # the rule only applies for n > 3 -- we need to hardcode the exception
            count += 2
            break
        if n % 2 == 0: # it is always best to divide even numbers by 2
            count += 1 
            n /= 2
        elif n % 4 == 1: # bit pattern 01 -- subtract 1 for bit pattern 00
            count += 1
            n -= 1
        elif n % 4 == 3: # bit pattern 11 -- add 1 for bit pattern 00 (with carry)
            count += 1
            n += 1
    
    # complexity: 
    ## it was easiest to think about this problem in terms of bits.
    ## at most every 2 operations is a bitshift.
    ## thus the loop will iterate at most 2*lg(n) times
    ## inside the loop are bitwise operations -- they take lg(n) time
    ## thus overall complexity is O(lg^2(n))
    ## further optimizations are possible, e.g. terminating if we know we're at a power of 2
    ## but these will not reduce the asymptotic complexity
    ## 
    
    
    return count
