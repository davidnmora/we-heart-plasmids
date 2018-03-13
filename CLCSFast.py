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

#TODO for both backtracks, check bounds!!
#Backtracking for upper bound. Should go LEFT when up and left are the same. Save the TOP
#node for vertical columns
def backtrackUpper(A, B, pathStartIndex, l, u):
	i = len(A)
	j = len(B)
	left = False
	while i >= 0 and j >= 0:
		#Diagonal
		if (i > 0 and j > 0):
			if (dpTable[pathStartIndex+i-1][j-1]+1 == dpTable[pathStartIndex+i][j]):
				upperMatrix[pathStartIndex][j] = i+pathStartIndex
				i -= 1
				j -= 1
			#Take the top node if top > left (for top, save the highest node)
			elif (dpTable[pathStartIndex+i-1][j] > dpTable[pathStartIndex+i][j-1]) :
				upperMatrix[pathStartIndex][j] = i+pathStartIndex
				i -= 1
			#If top and left are the same, take left
			elif (dpTable[pathStartIndex+i-1][j] == dpTable[pathStartIndex+i][j-1]):
				upperMatrix[pathStartIndex][j] = i+pathStartIndex
				j-=1
			#Otherwise left is bigger
			else:
				upperMatrix[pathStartIndex][j] = i+pathStartIndex
				j -= 1
		elif (j == 0 and i >= 0 and not left):
			#Only can go up
			upperMatrix[pathStartIndex][j] = i + pathStartIndex
			i -= 1
		elif (i == 0 and j >= 0):
			#Only can go left
			upperMatrix[pathStartIndex][j] = i+pathStartIndex
			j -= 1
			left = True

#Backtracking for the lower bound. Should go UP when up and left are the same. Save the BOTTOM
#node for vertical columns
def backtrackLower(A, B, pathStartIndex, l, u):
	i = len(A)
	j = len(B)
	top = False
	left = False
	while i >= 0 and j >= 0:
		if (i > 0 and j > 0):
			#Diagonal
			if (dpTable[pathStartIndex+i-1][j-1]+1 == dpTable[pathStartIndex+i][j]):
				lowerMatrix[pathStartIndex][j] = i+pathStartIndex
				i-=1
				j-=1
				top = False
			#If top is larger
			elif (dpTable[pathStartIndex+i-1][j] > dpTable[pathStartIndex+i][j-1]) :
				if not top:
					lowerMatrix[pathStartIndex][j] = i+pathStartIndex
				i -= 1
				top = True
			#If top and left are the same, take up
			elif (dpTable[pathStartIndex+i-1][j] == dpTable[pathStartIndex+i][j-1]):
				if not top:
					lowerMatrix[pathStartIndex][j] = i+pathStartIndex
				i-=1
				top = True
			#Otherwise left is bigger
			else:
				lowerMatrix[pathStartIndex][j] = i+pathStartIndex
				j -= 1
				top = False
		elif (j == 0 and i >= 0 and not left):
			#Can only go up
			i -= 1
		elif (i == 0 and j >= 0):
			#Can only go left
			lowerMatrix[pathStartIndex][j] = i+pathStartIndex
			left = True
			j -= 1



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
		# else take left

		# Update the lower and upperMatrix at column index 0 with pathStartIndex
		lowerMatrix[pathStartIndex][0] = pathStartIndex
		upperMatrix[pathStartIndex][0] = pathStartIndex
	return


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
	for row in range(1, m+1):
		for col in range(1,n+1):
			if AA[pathStartIndex+row-1] == B[col-1]:
				dpTable[row+pathStartIndex][col] = dpTable[pathStartIndex+row-1][col-1]+1
			else:
				dpTable[pathStartIndex+row][col] = max(dpTable[pathStartIndex+row-1][col], dpTable[pathStartIndex+row][col-1])
			# 2. BACKTRACCE TO STORE SHORTEST PATH IN lowerMatrix and upperMatrix
	#print dpTable
	results.append(dpTable[pathStartIndex+m][n])
	backtrackUpper(A,B,pathStartIndex,l,u)
	backtrackLower(A,B,pathStartIndex,l,u)
	#print upperMatrix
	#print lowerMatrix
	return

def findShortestPath(A, B, lowerMatrix, upperMatrix, l, u):
	#print "findShortestPath: l = %d, u = %d" % (l, u)
	if u - l <= 1:
		return
	mid = (l + u) / 2
	#print "mid: %d" % mid
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
		# SETUP: find initial bounding path before running recursive algorithm
		singleShortestPath(A, B, l, l, u, True)
		singleShortestPath(A, B, u, l, u, True)

		# THE REAL DEAL: run the algorithm
		findShortestPath(A, B, lowerMatrix, upperMatrix, l, u) # TO DO: return shortest path
		#Case if a string is only 1 letter long
		if u == 1:
			if A in B:
				results.append(1)
		shortestPath = max(results)
		print shortestPath
		#Clear the results array for the next problem
		del results[:]
	return

if __name__ == '__main__':
	main()
