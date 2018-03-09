import sys
import numpy as np
from cut import cut
from LCS import LCS

def CLCS(A,B):
	bestLCS = 0
	for i in range(len(A)):
		currLCS = LCS(cut(A, i), B)
		if currLCS > bestLCS:
			bestLCS = currLCS
			if bestLCS == len(A): # catches a perfect match
				return bestLCS
	return bestLCS

def main():
	if len(sys.argv) != 1:
		sys.exit('Usage: `python LCS.py < input`')
	
	for line in sys.stdin:
		A,B = line.split()
		print "SOLUTION: " + str(CLCS(A,B))
	return

if __name__ == '__main__':
	main()
