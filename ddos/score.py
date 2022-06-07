
#data = score of attacker after being reduced. Received from collect.sh file
#mac = attacker host, i.e. h1/h2/h3 .....
#n = variable to store the attacker index, i.e. h1 has index 1, h2 has index 2. This is to update the score at that particular index in the score.txt file


import sys
import json
data=json.loads(sys.argv[1])			
mac=sys.argv[2]
n=mac[1:]
n=int(n)
f=open("score.txt","r")
l=f.read()
l=l.split(',')
l[n-1]=data					#updates the score here
s=''
print "Updated score list is: ",l 
for i in range(len(l)-1):
	s+=str(l[i])+','
s+=l[len(l)-1]
f1=open("score.txt","w")
f1.write(s)
f1.close()


