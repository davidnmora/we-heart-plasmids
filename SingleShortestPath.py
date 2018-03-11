import sys
import numpy as np

lower_matrix = np.zeros((2048, 2048), dtype=int)
upper_matrix = np.zeros((2048, 2048), dtype=int)
arr = np.zeros((2*2048, 2048), dtype=int)

def SingleShortestPath(A, B, mid, p_lower, p_upper):
	m = len(A)
	n = len(B)

	for i in range(1, m+1):
		for j in range(1, n+1):
			if A[i-1]==B[j-1] and 