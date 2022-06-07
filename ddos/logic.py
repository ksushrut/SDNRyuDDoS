import sys
a=sys.argv[1]						#a = h1/h2/h3.....
a=int(a[1])							#a = 1/2/3.....
f=open("counter.txt","r+")			#counter file keep count of the number of times a host's score has fallen below threshold	
content=f.read()
l=content.split(',')				#l = ['0', '0', .....] i.e. list elements are string elements
l_int=[]
for i in range(len(l)):
	num=int(l[i])
	l_int.append(num)				#converting the string list into integer list
l_int[a-1]+=1						#increase the frequency coun by 1
s=''
for i in range(len(l_int)-1):
	s+=str(l_int[i])+','
s+=str(l_int[i])
print "Count of scores fallen below threshold: ",s
f.seek(0)
f.write(s)
f.truncate()
f.close()

