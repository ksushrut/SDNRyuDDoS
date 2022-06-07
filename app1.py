import checker
import subprocess
import os
apis=["curl -X GET http://localhost:8080/stats/switches","curl -X GET http://localhost:8080/stats/desc/1","curl -X GET http://localhost:8080/stats/port/1"]		#apis = list of apis the application wants to access
checker.checkapi(apis,1)						

'''
Passing the api list and the app number(1) to the checkapi function 
api are checked if the exist in the app1allow.txt file
app number is passed to change the score of app number
'''
