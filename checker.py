import subprocess
def checkapi(apilist,appno):				#apilist=list of apis the app wants to access
	f=open("app1allow.txt","r")			#opening the file containing the list of apis ALLOWED
	f1=open("app2allow.txt","r")
	api=f.read()
	api1=f1.read()
	l=[]							#api is a string variable containing the list of allowed APIs	
	for i in range(len(apilist)):		#traversing the list to get each api in api list
		if(apilist[i] in api or apilist[i] in api1):			#checking if the api in list is allowed in the file
			print "API accessed: ",apilist[i],"====>"
			subprocess.call(apilist[i],shell=True)		#run if lookup is found		
			print ""
			print ""
		else:
			print("API access denied!!!\n")
			f=open("appscore.txt","r")
			l=f.read()
			l=l.split(',')
			l[appno-1]=int(l[appno-1])-3
			f.close()
			f1=open("appscore.txt","w")
			s=""
			for i in range(len(l)-1):
				s+=str(l[i])+','
			s+=str(l[len(l)-1])
			f1.write(s)
			f1.close
			
			
