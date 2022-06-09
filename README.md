# SDNRyuDDoS

Files and their uses:
1. app1.py: Application 1 accessing certain APIs
2. app1allow.txt: List of allowed apis for app1
3. app2.py: Application 2 accessing certain APIs
4. app2allow.txt: List of allowed apis for app2
5. appscore.txt: Maintains score for apps
6. checker.py: Used to check which apis are allowed. Contains check function

Files in ddos:
1. customCtrl.py: A custom Ryu Controller
2. topo.py: Python file where topology is created.
3. collect.sh: Used to monitor the traffic
4. gentraffic.sh: Used to generae normal traffic
5. score.txt: Maintains score of the hosts
6. score.py: Updates the score of the host in score.txt file
7. score_increase.py: Used to increase the score of host if the score is below 100 and normal traffic is found in the network
8. create.txt: Used to create a counter.txt file
9. logic.py: Used to calculate the number of times theq score has fallen below the threshold
10. counter.txt: Maintains the number of times a host's score has fallen below the threshold
11. computerTuples.py: Used to calculate parameters for machine learning algorithm
12.inspector.py: Calls the model to classify the given characteristic values
13. realtime.csv: Contains 5 characteristic values.
14. dataset.csv: Dataset for prediction
15. svm.py: SVM to classify into attack or not an attack.

Steps to run:
Paste the ddosfolder in ryu folder.
Terminal 1: ryu-manager doos/customCtrl.py ryu.app.ofctl_rest
Terminal 2: cd ddos and then sudo python topo.py
Terminal 3: cd ddos and source collect.sh

*Make sure that the scores of host in score.txt are 100*
To generate normal traffic, in Terminal 2: <host> source gentraffic.sh    eg: h2 source gentraffic.sh
For ddos attack, in Terminal 2: <host> hping3 --rand-source --flood <target ip>     eg: h2 hping3 --rand-source --flood 10.0.0.1

In Terminal 4: sudo python app1.py      For API access

