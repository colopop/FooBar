def answer(data, n):
	#treating n==0 separately could improve performance with many workers
	if n == 0:
		return []

	from collections import Counter
	count = Counter()
	#first pass counts total occurrences
	for worker in data:
		count[worker] += 1
	#create and return the correct list
	return [w for w in data if count[w] < n]
