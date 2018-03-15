import sys
import numpy as np

MATRIX_SIZE = 2048

#Matrix to keep track of lower boundary paths
lowerMatrix = np.zeros((MATRIX_SIZE, MATRIX_SIZE), dtype=int)
#Matrix to keep track of upper boundary paths
upperMatrix = np.zeros((MATRIX_SIZE, MATRIX_SIZE), dtype=int)
#2mxn DP table
dpTable = np.zeros((2*MATRIX_SIZE, MATRIX_SIZE), dtype=int)
#Array to keep track of the results from each case, return the largest result
results = []

def isInBounds(row, col, lowerBoundPath, upperBoundPath):
	return (row >= upperBoundPath[col]) and (row <= lowerBoundPath[col])

#Backtracking for upper bound. Should go LEFT when up and left are the same. Save the TOP
#node for vertical columns
def backtrackUpper(A, B, pathStartIndex, l, u, first):
	i = len(A)
	j = len(B)
	while i > 0 and j > 0:
		#Take up
		if ((isInBounds(pathStartIndex+i-1, j, lowerMatrix[u], upperMatrix[l]) or first) and dpTable[pathStartIndex+i-1][j] == dpTable[pathStartIndex+i][j]):
			upperMatrix[pathStartIndex][j] = i+pathStartIndex
			i-=1

		#Diagonal
		elif ((isInBounds(pathStartIndex+i-1, j-1, lowerMatrix[u], upperMatrix[l]) or first) and dpTable[pathStartIndex+i-1][j-1]+1 == dpTable[pathStartIndex+i][j]):
			upperMatrix[pathStartIndex][j] = i+pathStartIndex
			i -= 1
			j -= 1
		#Take the Left step
		elif (isInBounds(pathStartIndex+i, j-1, lowerMatrix[u], upperMatrix[l]) or first) and dpTable[pathStartIndex+i][j-1] == dpTable[pathStartIndex+i][j]:
			upperMatrix[pathStartIndex][j] = i+pathStartIndex
			j-=1

	#For the cases when j or i is 0, but the other is not yet
	while i > 0  or j > 0:
		#Can only go up
		if (j == 0 and i > 0 and (isInBounds(pathStartIndex+i-1, j, lowerMatrix[u], upperMatrix[l]) or first)):
			upperMatrix[pathStartIndex][j] = i+pathStartIndex
			i -= 1
		elif i == 0 and j > 0 and (isInBounds(pathStartIndex+i, j-1, lowerMatrix[u], upperMatrix[l]) or first):
			#Only can go left
			upperMatrix[pathStartIndex][j] = i+pathStartIndex
			j -= 1
	#If we end right at i = 0 and j = 0
	if (i == 0 and j==0 and (isInBounds(pathStartIndex+i, j, lowerMatrix[u], upperMatrix[l]) or first)):
		upperMatrix[pathStartIndex][j] = i+pathStartIndex

#Backtracking for the lower bound. Should go UP when up and left are the same. Save the BOTTOM
#node for vertical columns
def backtrackLower(A, B, pathStartIndex, l, u, first):
	i = len(A)
	j = len(B)
	#Previous move was a vertical step up
	top = False
	while i > 0 and j > 0:
		#Take the diagonal
		if ((isInBounds(pathStartIndex+i-1, j-1, lowerMatrix[u], upperMatrix[l]) or first) and dpTable[pathStartIndex+i-1][j-1]+1 == dpTable[pathStartIndex+i][j]):
			if not top:
				lowerMatrix[pathStartIndex][j] = i+pathStartIndex
			i-=1
			j-=1
			top = False
		#Take left 
		elif (isInBounds(pathStartIndex+i, j-1, lowerMatrix[u], upperMatrix[l]) or first) and dpTable[pathStartIndex+i][j-1] == dpTable[pathStartIndex+i][j]:
			if not top:
				lowerMatrix[pathStartIndex][j] = i+pathStartIndex
			j-=1
			top = False
		#Take up 
		elif (isInBounds(pathStartIndex+i-1, j, lowerMatrix[u], upperMatrix[l]) or first) and dpTable[pathStartIndex+i-1][j] == dpTable[pathStartIndex+i][j]:
			if not top:
				lowerMatrix[pathStartIndex][j] = i+pathStartIndex
			i-=1
			top = True

	#For cases when one or the other is 0
	while i > 0 or j > 0:
		#Can only go up
		if (j == 0 and i > 0 and (isInBounds(pathStartIndex+i-1, j, lowerMatrix[u], upperMatrix[l]) or first)):
			#Can only go up
			if not top:
				lowerMatrix[pathStartIndex][j] = i+pathStartIndex
				top = True
			i -= 1
		elif (i == 0 and j > 0 and (isInBounds(pathStartIndex+i, j-1, lowerMatrix[u], upperMatrix[l]) or first)):
			#Can only go left
			lowerMatrix[pathStartIndex][j] = i+pathStartIndex
			j -= 1
	#If we end right at i = 0 and j = 0
	if (i == 0 and j==0 and (isInBounds(pathStartIndex+i, j, lowerMatrix[u], upperMatrix[l]) or first)):
		lowerMatrix[pathStartIndex][j] = i+pathStartIndex


#SingleShortestPath: updates the DP table for the values within the bounds, and then
#backtrack to get fill in the upper and lower paths for the matrices
def singleShortestPath(A,B, pathStartIndex, l, u, first):
	m = len(A)
	n = len(B)
	AA = A + A
	#Zero out the row of pathStartIndex
	dpTable[pathStartIndex] = 0
	dpTable[:,0] = 0
	# 1. FILL IN DP TABLE (within bounding constraints)
	# Start from upper[col] and lower[col]
	for row in range(1, m+1):
		for col in range(1,n+1):
			if (isInBounds(row+pathStartIndex, col, lowerMatrix[u], upperMatrix[l])) or first:
				if isInBounds(row+pathStartIndex-1, col-1, lowerMatrix[u], upperMatrix[l]) or first:
					#Check diagonal is within bounds
					if AA[pathStartIndex+row-1] == B[col-1]:
						dpTable[row+pathStartIndex][col] = dpTable[pathStartIndex+row-1][col-1]+1
						continue
				#Check if left and up is within bounds if can't take diagonal
				up = isInBounds(pathStartIndex+row-1, col, lowerMatrix[u], upperMatrix[l])
				left = isInBounds(pathStartIndex+row, col-1, lowerMatrix[u], upperMatrix[l])
				if (up and left) or first:
					dpTable[pathStartIndex+row][col] = max(dpTable[pathStartIndex+row-1][col], dpTable[pathStartIndex+row][col-1])
				elif up or first:
					#Top is in bounds, but left is not
					dpTable[pathStartIndex+row][col] = dpTable[pathStartIndex+row-1][col]
				elif left or first:
					#Left is in bounds, but up is not
					dpTable[pathStartIndex+row][col] = dpTable[pathStartIndex+row][col-1]
			# 2. BACKTRACE TO STORE SHORTEST PATH IN lowerMatrix and upperMatrix
	results.append(dpTable[pathStartIndex+m][n])
	backtrackUpper(A,B,pathStartIndex,l,u, first)
	backtrackLower(A,B,pathStartIndex,l,u, first)
	return

def findShortestPath(A, B, lowerMatrix, upperMatrix, l, u):
	if u - l <= 1:
		return
	mid = (l + u) / 2
	singleShortestPath(A, B, mid, l, u, False)
	findShortestPath(A, B, lowerMatrix, upperMatrix, l, mid)
	findShortestPath(A, B, lowerMatrix, upperMatrix, mid, u)
	return

def main():
	if len(sys.argv) != 1:
		sys.exit('Usage: `python CLCSFast.py < input`')
	
	for l in sys.stdin:
		A,B = l.split()
		p = np.zeros(len(A), dtype=int)
		l = 0
		u = len(A)

		#Case if string A is a substring of B
		if A in B:
			results.append(len(A))
		elif B in A:
			results.append(len(B))
		else:
			# SETUP: find initial bounding path before running recursive algorithm
			singleShortestPath(A, B, l, l, u, True)
			singleShortestPath(A, B, u, l, u, True)

			# THE REAL DEAL: run the algorithm
			findShortestPath(A, B, lowerMatrix, upperMatrix, l, u) # TO DO: return shortest pat

		shortestPath = max(results)
		print shortestPath
		#Clear the results array for the next problem
		del results[:]
	return

if __name__ == '__main__':
	main()
