import checker
import subprocess
import os
apis=["curl -X GET http://localhost:8080/stats/tablefeatures/1","curl -X GET http://localhost:8080/stats/table/2","curl -X GET http://localhost:8080/stats/aggregateflow/1"]
checker.checkapi(apis,2)						

'''
Passing the api list and the app number(1) to the checkapi function 
api are checked if the exist in the app1allow.txt file
app number is passed to change the score of app number
'''
