def answer(l):
   #at first I was certain this was a modified version of subset-sum, but I'm pretty sure the following is easier to follow and has superior performance.
   #subset sum would be O(n^2) or even O(n^3) depending on the exact implementation. the following is O(n * lg n).
   #first, a little function to turn a list into a number
   #note -- this will "reverse" the number. but that's fine because it works well with the rest of the code
   def to_int(ls):
      ans = 0
      for i in range(len(ls)):
         ans += ls[i]*pow(10,i)
      return ans
   #since a number is divisible by three iff the sum of its digits is divisible by three, order does not matter
   #therefore we should sort a given subset to get the largest possible number from it (largest number in highest decimal place, etc)
   l.sort()
   #first we find the sum modulo 3 of the digits
   dsum = sum(l) % 3

   #this can be 0, 1, or 2
   #if it's 0, the number made from the whole set is already divisible by three
   #note: this will also catch the empty list
   if dsum == 0:
      return to_int(l)

   #if it's 1, we can make it 0 in two ways
   #first, we can remove a single number that equals 1 mod 3
   #if there is no such number, we can remove two numbers that equal 2 mod 3
   #if there is no such pair, there is no solution
   #obviously we want to remove as few digits as possible, and prioritize the smallest ones
   #thus we will try to remove a 1 before trying to remove the 2s, and we will go from smallest to largest
   if dsum == 1:
      #seek a number that is 1 mod 3 and remove it
      for i in range(len(l)):
         if l[i] % 3 == 1:
            del l[i]
            return to_int(l)

      #if we got here, we failed to find a 1
      #now let's check for twos -- this logic needs to look a bit different
      #we'll create a new list with two items
      newl = []
      two_count = 0
      for item in l:
         if item % 3 != 2 or two_count >= 2:
            newl.append(item)
         else:
            two_count += 1
      #if our new list is exactly two shorter, we can return that. otherwise we failed.
      if len(newl) + 2 == len(l):
         return to_int(newl)
      else:
         return 0

   #finally, we have the case dsum == 2
   #very similar to the previous code. we can reach 0 by removing two 1s or one 2.
   #again, we prefer losing fewer digits and smaller ones. so we check the 2 first and search from smallest to largest.
   #with a few swapped digits, this is identical to the previous code
   if dsum == 2:
      #seek a number that is 2 mod 3 and remove it
      for i in range(len(l)):
         if l[i] % 3 == 2:
            del l[i]
            return to_int(l)

      #if we got here, we failed to find a 1
      #now let's check for twos -- this logic needs to look a bit different
      #we'll create a new list with two items
      newl = []
      one_count = 0
      for item in l:
         if item % 3 != 1 or one_count >= 2:
            newl.append(item)
         else:
            one_count += 1
      #if our new list is exactly two shorter, we can return that. otherwise we failed.
      if len(newl) + 2 == len(l):
         return to_int(newl)
      else:
         return 0

if __name__ == "__main__":
   from random import randint
   lst = [randint(0,9) for x in range(randint(0,12))]
   lst = [7,2,5]
   print lst
   print sum(lst) % 3
   print answer(lst)
