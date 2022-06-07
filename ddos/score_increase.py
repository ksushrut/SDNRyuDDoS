f=open("score.txt","r+")
data=f.read()
data=data.split(',')
for i in range(len(data)):
	data[i]=int(data[i])
	if(data[i]<100):
		data[i]+=1
s=''
for i in range(len(data)-1):
	s+=str(data[i])+','
s+=str(data[i])
f.seek(0)
f.write(s)
