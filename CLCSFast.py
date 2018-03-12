import sys
import numpy as np

MATRIX_SIZE = 6

lowerMatrix = np.zeros((MATRIX_SIZE, MATRIX_SIZE), dtype=int)
upperMatrix = np.zeros((MATRIX_SIZE, MATRIX_SIZE), dtype=int)
dpTable = np.zeros((2*MATRIX_SIZE, MATRIX_SIZE), dtype=int)

def isInBounds(row, col, lowerBoundPath, upperBoundPath):
	return (row >= upperBoundPath[col]) and (row <= lowerBoundPath[col])

def backtrackAndStorePath(B, pathStartIndex, l, u):
	# start at end, insert into lowerMatrix and upperMatrix as you go
	row  = pathStartIndex

	for col in range(len(B), 1, -1):
		# TO DO: check bounds
		# update variables
		top  = dpTable[row-1][col]
		left = dpTable[row]  [col-1]
		diag = dpTable[row-1][col-1]
		curr = dpTable[row]  [col]
		
		# UPDATE lower and upper matrixes
		lowerMatrix[pathStartIndex][col] = row
		upperMatrix[pathStartIndex][col] = row # can be overwritten by vertical movements

		if diag+1 == curr:
			# take diagonal
			print("In diagonal case")
			row -= 1
		elif top > left:
			# take top until we take left or diag
			while True:
				row -= 1
				curr = dpTable[row][col]
				top  = dpTable[row-1][col]
				left = dpTable[row][col-1]
				diag = dpTable[row][col-1]
				if (diag+1 == curr) or (left > top):
					break
			# Update the upperMatrix with the "highest" (smallest) number after moving up vertically
			upperMatrix[pathStartIndex][col] = row
		print("row: ", row)
		# else take left

		# Update the lower and upperMatrix at column index 0 with pathStartIndex
		lowerMatrix[pathStartIndex][0] = pathStartIndex
		upperMatrix[pathStartIndex][0] = pathStartIndex
	return


#SingleShortestPath: updates the DP table for the values within the bounds, and then
#backtrack to get fill in the upper and lower paths for the matrices
def singleShortestPath(A,B, pathStartIndex, l, u):
	m = len(A)
	n = len(B)
	# 1. FILL IN DP TABLE (within bounding constraints)
	for row in range(1, m+1):
		for col in range(1,n+1):
			print(row, col)
			if isInBounds(row, col, lowerMatrix[l], upperMatrix[u]):
				if A[row-1] == B[col-1]:
					dpTable[row+pathStartIndex][col] = dpTable[pathStartIndex+row-1][col-1]+1
				else:
					dpTable[pathStartIndex+row][col] = max(dpTable[pathStartIndex+row-1][col], dpTable[pathStartIndex+row][col-1])
			# 2. BACKTRACCE TO STORE SHORTEST PATH IN lowerMatrix and upperMatrix
	print dpTable
	backtrackAndStorePath(B, pathStartIndex, l, u)
	return

def findShortestPath(A, B, lowerMatrix, upperMatrix, l, u):
	print "findShortestPath: l = %d, u = %d" % (l, u)
	if l - u <= 1:
		return
	mid = (l + u) / 2
	print "mid: %d" % mid
	singleShortestPath(A, B, mid, l, u)
	findShortestPath(A, B, lowerMatrix, upperMatrix, l, mid)
	findShortestPath(A, B, lowerMatrix, upperMatrix, mid, u)
	return

def main():
	if len(sys.argv) != 1:
		sys.exit('Usage: `python CLCSFast.py < input`')
	
	for l in sys.stdin:
		A,B = l.split()
		p = np.zeros(len(A), dtype=int)
		l = len(A)
		u = 0
		# SETUP: find initial bounding path before running recursive algorithm
		singleShortestPath(A, B, l, l, u)
		singleShortestPath(A, B, u, l, u)

		# THE REAL DEAL: run the algorithm
		findShortestPath(A, B, lowerMatrix, upperMatrix, l, u) # TO DO: return shortest path
	return

if __name__ == '__main__':
	main()
