import sys
import numpy as np

def singleShortestPath(A,B, pathStartIndex, lowerBoundPath, upperBoundPath):
	arr = np.zeros((2048, 2048), dtype=int)
	m = len(A)
	n = len(B)

	for i in range(1,m+1):
		for j in range(1,n+1):
			if A[i-1] == B[j-1]:
				arr[i][j] = arr[i-1][j-1]+1
			else:
				arr[i][j] = max(arr[i-1][j], arr[i][j-1])

	# TO DO: store upper and lower path in their respective matrixes
	return arr[m][n]

def findShortestPath(A, B, p, l, u):
	print p
	if u - l <= 1:
		return
	mid = (l + u) / 2
	print "mid: %d" % mid
	p[mid] = singleShortestPath(A, B, mid, p[l], p[u])
	findShortestPath(A, B, p, l, mid)
	findShortestPath(A, B, p, mid, u)

def main():
	if len(sys.argv) != 1:
		sys.exit('Usage: `python CLCSFast.py < input`')
	
	for l in sys.stdin:
		A,B = l.split()
		p = np.zeros(len(A), dtype=int)
		l = 0
		u = len(A) - 1
		# find initial bounding path
		zeros = np.zeros(len(B), dtype=int)
		uppers = np.full(2, len(A), dtype=int)
		p[0] = singleShortestPath(A, B, l, zeros, uppers)
		p[u] = singleShortestPath(A, B, u, zeros, uppers)
		findShortestPath(A, B, p, l, u) # TO DO: return shortest path
	return

if __name__ == '__main__':
	main()
