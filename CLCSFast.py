import sys
import numpy as np

lowerMatrix = np.zeros((2048, 2048), dtype=int)
upperMatrix = np.zeros((2048, 2048), dtype=int)
dpTable = np.zeros((2*2048, 2048), dtype=int)
#SingleShortestPath: updates the DP table for the values within the bounds, and then
#backtrack to get fill in the upper and lower paths for the matrices
def singleShortestPath(A,B, pathStartIndex, lowerBoundPath, upperBoundPath):
	#dpTable = np.zeros((2048, 2048), dtype=int)
	m = len(A)
	n = len(B)
	# 1. FILL IN DP TABLE (within bounding constraints)
	for i in range(1,m+1):
		for j in range(1,n+1):
			if A[i-1] == B[j-1]:
				dpTable[i][j] = dpTable[i-1][j-1]+1
			else:
				dpTable[i][j] = max(dpTable[i-1][j], dpTable[i][j-1])
	# 2. BACKTRACCE TO STORE SHORTEST PATH IN lowerMatrix and upperMatrix
	return

def findShortestPath(A, B, p, l, u):
	print p
	if u - l <= 1:
		return
	mid = (l + u) / 2
	print "mid: %d" % mid
	p[mid] = singleShortestPath(A, B, mid, p[l], p[u])
	findShortestPath(A, B, p, l, mid)
	findShortestPath(A, B, p, mid, u)
	return

def main():
	if len(sys.argv) != 1:
		sys.exit('Usage: `python CLCSFast.py < input`')
	
	for l in sys.stdin:
		A,B = l.split()
		p = np.zeros(len(A), dtype=int)
		l = 0
		u = len(A) - 1
		# find initial bounding path
		upperMatrix[l] = np.zeros(len(B), dtype=int)
		lowerMatrix[u] = np.full(2, len(B), dtype=int)
		singleShortestPath(A, B, l, zeros, uppers)
		singleShortestPath(A, B, u, zeros, uppers)
		findShortestPath(A, B, p, l, u) # TO DO: return shortest path
	return

if __name__ == '__main__':
	main()
