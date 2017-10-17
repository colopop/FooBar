def answer(src, dest):
    #a quick helper function will make everything easier
    def moves(s):
        #returns all legal moves from the source position
        moves = []
        if s % 8 <= 5: #out of bounds to the right
        	if s >= 8: #bottom row cannot do this move
        		moves.append(s-6)
        	if s <= 55: #top row cannot do this move
        		moves.append(s+10)
        if s % 8 <= 6: #out of bounds to the right
        	if s >= 16: #bottom two rows cannot do this move
        		moves.append(s-15)
        	if s <= 47: #top two rows cannot do this move
        		moves.append(s+17)
        if s % 8 >= 2: #out of bounds to the left
        	if s >= 8: #bottom row cannot do this move
        		moves.append(s-10)
        	if s <= 55: #top row cannot do this move
        		moves.append(s+6)
        if s % 8 >= 1: #out of bounds to the right
        	if s >= 16: #bottom two rows cannot do this move
        		moves.append(s-17)
        	if s <= 47: #top two rows cannot do this move
        		moves.append(s+15)
        return moves

    #we can use dynamic programming/Dijkstra's algorithm
    #the value of opt[square] is the minimum number of moves it takes to get to square from src
    #at the end, we can check opt[dest]
    dist = [65]*64
    dist[src] = 0
    #we will make several passes through the chessboard, updating the squares. the correct values will propagate out from src.
    passes = 0
    for i in range(6):
    	flag = True
    	for item in dist:
    		if item >= 65:
    			flag = False
    	if not flag:
    		passes += 1
    	for j in range(64):
    		#check all of the places that can move to j. the fastest path to j is the 1 + the best path to a source of j.
    		#the exception is src. opt[src] is 0.
    		if j == src:
    			continue
    		dist[j] = 1+min([dist[x] for x in moves(j)])

    return passes
