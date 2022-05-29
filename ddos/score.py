import sys
import json
data=json.loads(sys.argv[1])
mac=sys.argv[2]
print(mac)
n=mac[1:]
n=int(n)
f=open("score.txt","r")
l=f.read()
l=l.split(',')
l[n-1]=data
s=''
print(l)
for i in range(len(l)-1):
	s+=str(l[i])+','
s+=l[len(l)-1]
f1=open("score.txt","w")
f1.write(s)
f1.close()


