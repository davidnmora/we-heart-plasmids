import sys
import numpy as np
from cut import cut
from LCS import LCS

def main():
	print "CUT TEST: " + cut("yayPUTMEFIRST", 3)
	if len(sys.argv) != 1:
		sys.exit('Usage: `python LCS.py < input`')
	
	for l in sys.stdin:
		A,B = l.split()
		print LCS(A,B)
	return

if __name__ == '__main__':
	main()
