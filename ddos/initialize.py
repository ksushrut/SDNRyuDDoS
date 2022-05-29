import sys
a=sys.argv[1]
a=int(a[1])
f=open("score.txt","w")
for i in range(a):
	

print(content)
l=content.split(',')
print(l)
l_int=[]
for i in range(len(l)):
	num=int(l[i])
	l_int.append(num)
print("Int: ",l_int)
l_int[a-1]+=1
s=''
for i in range(len(l_int)-1):
	s+=str(l_int[i])+','
s+=str(l_int[i])
f.seek(0)
f.write(s)
f.truncate()
f.close()

