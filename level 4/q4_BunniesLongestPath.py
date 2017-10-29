def answer(times, time_limit):
    # this will be helpful: name the entrance and bulkhead locations
    start = 0
    bulkhead = len(times)-1
    # since we don't care about recovering a path, we can think in terms of "best time to node" rather than trying to go edge by edge
    # we don't want the cost of reaching a node directly, we want the lowest-cost way to reach it
    def getBestTimes(node):
        # Bellman-Ford
        pathcost = [9999999]*len(times)
        pathcost[node] = 0
        for i in range(len(times)-1):
            for node_idx, node in enumerate(times):
                for edge_idx, edge_len in enumerate(node): 
                    if pathcost[node_idx] + edge_len < pathcost[edge_idx]:
                        if node_idx == edge_idx:
                            continue
                        #otherwise Bellman-Ford as normal
                        pathcost[edge_idx] = pathcost[node_idx] + edge_len
        return pathcost

    # for each node, we should keep track of its best path to each other node
    BestPath = []
    for i in range(len(times)):
        BestPath.append(getBestTimes(i))

    # if there is a negative cycle, we can build up an arbitrarily large amount of time
    # thus we can always rescue all the bunnies
    # we check for a negative cycle here
    for node_idx, node in enumerate(times):
        for edge_idx, edge_len in enumerate(node):
            if BestPath[start][node_idx] + edge_len < BestPath[start][edge_idx]:
                # negative cycle!
                return list(range(len(times)-2))

    # we need some more tools
    from itertools import permutations
    def subsets(s):
        result = [[]]
        for item in s:
            result = result + [item2 + [item] for item2 in result]
        return result

    # here's the main algorithm
    # we'll store all sets of bunnies we're able to rescue and pick the best later
    possibilities = []
    for subset in subsets(range(len(times)-2)): 
        # try every subset of bunnies to rescue
        orders = permutations(subset)
        # for each subset, we'll try to visit them as cheaply as possible
        # this means taking the cheapest path to each one
        # but order matters when determining the total cost of the path
        # so we'll just try every order
        for order in orders:
            if len(order) == 0: continue # skip degenerate case
            
            # initial cost
            cost = BestPath[start][order[0]+1] 
            
            for i, bunny in enumerate(order):
                if i == 0: continue
                # add the cost to get to the next bunny
                cost += BestPath[order[i-1]+1][bunny+1] 
            
            # make sure we can still escape
            cost += BestPath[order[-1]+1][bulkhead] #cheapest cost from the last bunny to the bulkhead
            
            # this was the cheapest way to reach these bunnies in this order and get to the bulkhead
            # if we still can't make it, then we can't rescue this set of bunnies in this order
            if cost <= time_limit:
                # we'll get duplicates if multiple permutations are valid
                # but that's ok, we're talking at most hundreds of possibilities
                possibilities.append(sorted(order))
    
    if len(possibilities) == 0:
        return []
    
    else:
        # get the maximum-length solution
        maxlen = max([len(x) for x in possibilities])
        #if there are multiple max-length solutions, find the minimum-index one
        return min([i for i in possibilities if len(i) == maxlen])
