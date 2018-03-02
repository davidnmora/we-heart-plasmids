import sys

def verify(actual, expected):
	failed = 0
	for i in range(len(actual)):
		if actual[i] != expected[i]:
			print ("Test case #%d failed. Expected: %d; Actual %d" % (i+1, expected[i], actual[i]))
			failed += 1

	print ("---------------------------------")
	if failed == 0:
		print ("Passed all test cases!")
	else:
		print ("Failed %d/%d test cases." % (failed, len(actual)))
	print ("---------------------------------")

def main():
	if len(sys.argv) != 2:
		sys.exit("Usage: `python judge.py EXPECTED < ACTUAL")

	actual = [int(l) for l in sys.stdin]

	expected = None
	with open(sys.argv[1], 'r') as f:
		expected = ([int(l) for l in f])

	if len(actual) != len(expected):
		sys.exit("Error: The expected and actual outputs different lengths")

	verify(actual, expected)

if __name__ == '__main__':
	main()
