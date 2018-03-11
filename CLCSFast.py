import sys
import numpy as np

MATRIX_SIZE = 2048

lowerMatrix = np.zeros((MATRIX_SIZE, MATRIX_SIZE), dtype=int)
upperMatrix = np.zeros((MATRIX_SIZE, MATRIX_SIZE), dtype=int)
dpTable = np.zeros((2*MATRIX_SIZE, MATRIX_SIZE), dtype=int)
#SingleShortestPath: updates the DP table for the values within the bounds, and then
#backtrack to get fill in the upper and lower paths for the matrices
def singleShortestPath(A,B, pathStartIndex, lowerBoundPath, upperBoundPath):
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

def findShortestPath(A, B, lowerMatrix, upperMatrix, l, u):
	print "findShortestPath: l = %d, u = %d" % (l, u)
	if l - u <= 1:
		return
	mid = (l + u) / 2
	print "mid: %d" % mid
	singleShortestPath(A, B, mid, lowerMatrix[l], upperMatrix[u])
	findShortestPath(A, B, lowerMatrix, upperMatrix, l, mid)
	findShortestPath(A, B, lowerMatrix, upperMatrix, mid, u)
	return

def main():
	if len(sys.argv) != 1:
		sys.exit('Usage: `python CLCSFast.py < input`')
	
	for l in sys.stdin:
		A,B = l.split()
		p = np.zeros(len(A), dtype=int)
		l = len(A) - 1
		u = 0
		# SETUP: find initial bounding path before running recursive algorithm
		singleShortestPath(A, B, l, lowerMatrix[l], upperMatrix[u])
		singleShortestPath(A, B, u, lowerMatrix[l], upperMatrix[u])

		# THE REAL DEAL: run the algorithm
		findShortestPath(A, B, lowerMatrix, upperMatrix, l, u) # TO DO: return shortest path
	return

if __name__ == '__main__':
	main()
