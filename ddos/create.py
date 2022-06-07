import sys
n=sys.argv[1]
f=open("counter.txt","w")
for i in range(1,int(n)):
	f.write("0,")
f.write("0")
f.close()

