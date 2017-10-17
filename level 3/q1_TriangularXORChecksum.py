def answer(start, length):
    
    #first a function that gets the checksum of the sequence 0..x
    def getChecksum(first, last):

        def helper(x):
            if x%4 == 0:
                return x
            if x%4 == 1:
                return 1
            if x%4 == 2:
                return x+1
            if x%4 == 3:
                return 0

        return helper(last)^helper(first-1)
    
    #now we just xor the checksums of the selected minions row-by-row. we can do this because xor is associative. 
    #this function will end up being O(length) -- or O(sqrt(highest minion #)).
    ans = 0
    for i in range(length):
        ans ^= getChecksum(start + i*length, start + (i+1)*(length-1))

    return ans
