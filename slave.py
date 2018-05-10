import time
import modules
import numpy as np
import sys
import zmq


system_ip = "192.168.0.132"

port = "5560"
# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)
print "Collecting updates from server..."
socket.connect ("tcp://"+system_ip+":%s" % port)
topicfilter = sys.argv[1]
print ("filter:",topicfilter)
socket.setsockopt(zmq.SUBSCRIBE, topicfilter)



port = "5659"
context_results = zmq.Context()
socket_results = context_results.socket(zmq.PUB)
socket_results.connect("tcp://"+system_ip+":%s" % port)

def processMessage(msg):
	# print msg
	msgArray = modules.str2arr(msg)
	N = (len(msgArray) - 1)/2
	elements = []
	for i in range(0, (len(msgArray)-1), N/2):
		elements.append(msgArray[i:i+N/2])
	elements = np.array(elements)
	answer = np.dot(elements[0],elements[1]) + np.dot(elements[2],elements[3])
	answer = np.concatenate((answer,[msgArray[-1]]),axis=0)
	print "\nANS:"
	print answer,"\n"
	# print (9, modules.arr2str(answer))
	socket_results.send("%d %s" % (9, modules.arr2str(answer)))

while True:
	string = socket.recv()
	# print "\n"*3,string,"\n"*3
	# topic, messagedata = string.split()
	messagedata = string[2:]
	msg = messagedata
	processMessage(msg)

