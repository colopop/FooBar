def answer(M, F):
    #the trick here is to think of the bomb growth possibilities like a binary tree
    #at each node (a,b), you can either go to child (a+b,b) or child (a,a+b)
    #so from (m,f) we need to find our way backwards to (1,1)
    #but that's easy in principle, because we have exactly one path back since there's one parent at each step of the tree
    #for a child (a,b), the parent is (a,b-a) if b>a and (a-b,b) if a>b
    #the trouble is that when the search tree gets large, going back one step at a time won't cut it
    #that's O(max(M,F)), and when one of those is 10^50, we're in trouble
    #we need a better way
    
    M = long(M)
    F = long(F)
    
    #observation: GCD is always 1
    #this is because gcd(1,1)=1 and if gcd(a,b)=1 then gcd(a,a+b)=1
    #proof: let ap+bq=1. let p=p'+q. then a(p'+q)+bq=ap'+(a+b)q=1. thus gcd(a,a+b)=1.
    #that lets us cut out the impossible ones pretty easily
    from fractions import gcd
    if gcd(M,F) != 1:
        return "impossible"
    
    #cover some easy cases that break the below code slightly
    if M == 1 and F == 1:
        return 0
    if M == 1:
        return F-1
    if F == 1:
        return M-1
    
    #here's the main trick: instead of going step by step, we can make big jumps
    #(a-b,b) is the parent of (a,b), but if a-b is still > b, the grandparent is (a-b-b,b)
    #and so on until we finally get the first term to be smaller than b
    #we can make that whole jump in one step
    #the definition of a/b is the number of times you can subtract b from a before you hit zero
    #thus the number of generations it takes to get there is a/b (integer division)
    #and the value you're left with after that is a%b
    gens = 0
    while M > 1 and F > 1:
        
        #we can do this funky Eucid's-algorithm-like thing
        if M > F:
            gens += M / F #integer division
            M = M % F #shortcut for repeated subtraction by F until M < F
        else:
            gens += F / M #integer division
            F = F % M #shortcut for repeated subtraction by F until F < M
            
        #if either value hits 1, we can get the answer in one step
        if M == 1:
            gens += F - 1
            break
        if F == 1:
            gens += M - 1
            break
    
    #to figure out worst case complexity, let's assume WLOG that M>F
    #let's try to figure out the most convenient F
    #since we want to maximize the number of steps, we don't want to just maximize M%F.
    #we want to an M%F that does for F what F does for M.
    #using - instead of % since we're guaranteed M>F:
    #we want F = (1/n)*M such that (M-F)=(1/n)*F
    #solving for n gets us n=sqrt(M/(M-F))
    #whatever this is, it's a constant ratio. and reducing M by a constant ratio until we reach 1 will terminate in log(M) time
    #so the complexity of this solution is O(log(max(M,F)))
        
    return gens
