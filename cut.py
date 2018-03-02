def cut(string, cutBeforeThisIndex):
	return string[cutBeforeThisIndex:] + string[:cutBeforeThisIndex]

string = "abcd"

print "\nOutput:\n" + cut(string, 2)

# any integer k
k = 8
print "\K mod n:\n" + cut(string, 8 % len(string))