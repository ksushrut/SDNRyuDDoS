#!/bin/bash
n=6    # number of switches
h=9
port=1
threshold=80
python create.py "${h}"	#create.py is used to create counter.txt which keeps count of the no of times an attack has occured and which is the attacker
i=1 #iterating variable
l=`python read.py`	#read from counte.txt

scores=$(echo $l | tr ";" "\n")
IFS=','
read -a arr <<<"$l" #reading str as an array as tokens separated by IFS  


#dictionary to store score of each host
declare -A score_dict
score_dict[0a:0a:00:00:00:01]=${arr[0]}		
score_dict[0a:0a:00:00:00:02]=${arr[1]}
score_dict[0a:0a:00:00:00:03]=${arr[2]}
score_dict[0a:0a:00:00:00:04]=${arr[3]}
score_dict[0a:0a:00:00:00:05]=${arr[4]}
score_dict[0a:0a:00:00:00:06]=${arr[5]}
score_dict[0a:0a:00:00:00:07]=${arr[6]}
score_dict[0a:0a:00:00:00:08]=${arr[7]}
score_dict[0a:0a:00:00:00:09]=${arr[8]}

#dictionary to map mac address to the host
declare -A mac_dict
mac_dict[0a:0a:00:00:00:01]=h1
mac_dict[0a:0a:00:00:00:02]=h2
mac_dict[0a:0a:00:00:00:03]=h3
mac_dict[0a:0a:00:00:00:04]=h4
mac_dict[0a:0a:00:00:00:05]=h5
mac_dict[0a:0a:00:00:00:06]=h6
mac_dict[0a:0a:00:00:00:07]=h7
mac_dict[0a:0a:00:00:00:08]=h8
mac_dict[0a:0a:00:00:00:09]=h9

for i in {1..2000}
do
    for ((j = 1; j <= n; j++))
    do
        echo "Inspection at s$j"			#echo "Inspection no. $i at s$j"
        # extract essential data from raw data
        sudo ovs-ofctl dump-flows s$j > data/raw
        grep "nw_src" data/raw > data/flowentries.csv
        packets=$(awk -F "," '{split($4,a,"="); print a[2]","}' data/flowentries.csv)
        bytes=$(awk -F "," '{split($5,b,"="); print b[2]","}' data/flowentries.csv)
        ipsrc=$(awk -F "," '{out=""; for(k=2;k<=NF;k++){out=out" "$k}; print out}' data/flowentries.csv | awk -F " " '{split($11,d,"="); print d[2]","}')
        ipdst=$(awk -F "," '{out=""; for(k=2;k<=NF;k++){out=out" "$k}; print out}' data/flowentries.csv | awk -F " " '{split($12,d,"="); print d[2]","}')
        macsrc=$(awk -F "," '{out=""; for(k=2;k<=NF;k++){out=out" "$k}; print out}' data/flowentries.csv | awk -F " " '{split($9,d,"="); print d[2]}')
        macdst=$(awk -F "," '{out=""; for(k=2;k<=NF;k++){out=out" "$k}; print out}' data/flowentries.csv | awk -F " " '{split($10,d,"="); print d[2]}')
        
        # check if there are no traffics in the network at the moment.
        
        if test -z "$packets" || test -z "$bytes" || test -z "$ipsrc" || test -z "$ipdst" 
        then
            state=0
        else	
		        echo "$packets" > data/packets.csv
		        echo "$bytes" > data/bytes.csv
		        echo "$ipsrc" > data/ipsrc.csv
		        echo "$ipdst" > data/ipdst.csv	
		        printf "$macsrc" > data/macsrc.txt
		        python3 computeTuples.py
		        python3 inspector.py
		        state=$(awk '{print $0;}' .result)				#state = 0(no attack) or 1(attack)
		        
		        #the next condition checks if any of the host score is less than 100, if yes then increase using score_increase.py file.
		        
				if [[ ${score_dict[0a:0a:00:00:00:01]} != "100" || ${score_dict[0a:0a:00:00:00:02]} != "100" || ${score_dict[0a:0a:00:00:00:03]} != "100" || ${score_dict[0a:0a:00:00:00:04]} != "100" || ${score_dict[0a:0a:00:00:00:05]} != "100" || ${score_dict[0a:0a:00:00:00:06]} != "100" || ${score_dict[0a:0a:00:00:00:07]} != "100" || ${score_dict[0a:0a:00:00:00:08]} != "100" || ${score_dict[0a:0a:00:00:00:09]} != "100" ]]
        		then		    		
					python score_increase.py			
		    	fi       
        fi

        if [ $state -eq 1 ];			#if attack is detected
        then
            file='data/macsrc.txt'
            echo "------------------------------------------"
            echo "Network is under attack occuring at s$j"            
            while read line; do   
				attacker=$line
				i=$((i+1))  
				done < $file
				att=${mac_dict[$attacker]}
	    		echo "Attacker is ${mac_dict[$attacker]}"
				if [ ${score_dict[$attacker]} -gt $threshold ]		## if less than 80, suspend
				then
				    
				    	############################# LOGIC FOR THRESHOLD #####################
				    	
				    	score_dict[$attacker]=$((score_dict[$attacker]-9))			#reduce score by 9
				    	echo "Current score of the attacker is: $((score_dict[$attacker]))"			#print score
				    	python score.py "${score_dict[$attacker]}" "$att"			#pass score and attacker host to score.py file to update in file
				    	sudo ovs-ofctl mod-port s$j $port no-receive				#suspend the port
				    	sleep 5														#wait for 5 seconds
				    	echo "Port suspended for 5 sec"	      						
    					echo "------------------------------------------"  	
				    	sudo ovs-ofctl mod-port s$j $port receive					#enable the port again
				else
					    python logic.py "${att}"									#logic.py keeps a count of attacks
				    	echo -e "Score has fallen below threshold! Intervention of admin required\n"
				    	sudo ovs-ofctl mod-port s$j $port down						#down the port
				    	sudo ovs-ofctl dump-flows s$j > data/rawblock				
				    	echo "Admin, enter your decision, 0 to block, 1 to allow"
				    	read choice													#0(keep it blocked), 1(allow to run)
				    	if [ $choice -eq 1 ]
				    	then
				    		sudo ovs-ofctl mod-port s$j $port up					
				    		score_dict[$attacker]=100
				    		python score.py "${score_dict[$attacker]}" "$att"
				    	else
				    		echo "BLOCKED!!!!"
				    		sudo ovs-ofctl dump-flows s$j > data/rawblock2
				    	fi															#end of if(choice by admin)
            	fi																	#end of if(threshold)
                                                       
            default_flow=$(sudo ovs-ofctl dump-flows s$j | tail -n 1)    # Get flow ] "action:CONTROLLER:<port_num>" sending unknown packet to the controller
            sudo ovs-ofctl del-flows s$j
            sudo ovs-ofctl add-flow s$j "$default_flow"
        fi																			#end of if(attack is detected)
    done
    sleep 3
done



# ==============================================================================================================================================
# Ref
# Get all fields (n columns) in awk: https://stackoverflow.com/a/2961711/11806074
# e.g. awk -F "," '{out=""; for(i=2;i<=NF;i++){out=out" "$i" "i}; print out}' data/flowentries.csv 

# ovs-ofctl reference
# add-flow SWITCH FLOW        add flow described by FLOW    e.g. ... add-flow s1 "flow info"
# add-flows SWITCH FILE       add flows from FILE           e.g. ... add-flows s1 flows.txt

# example of multiple commands in awk, these commands below extract ip_src and ip_dst from flow entries
# awk -F "," '{split($10,c,"="); print c[2]","}' data/flowentries.csv > data/ipsrc.csv
# awk -F "," '{split($11,d,"=");  split(d[2],e," "); print e[1]","}' data/flowentries.csv > data/ipdst.csv
