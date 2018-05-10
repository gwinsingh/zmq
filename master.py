import time, pickle
import numpy as np
import modules
# many senders
import zmq
import sys


system_ip = "192.168.0.132"


port = "5559"
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.connect("tcp://"+system_ip+":%s" % port)

port = "5660"
# Socket to talk to server
context_results = zmq.Context()
socket_results = context_results.socket(zmq.SUB)
print "Collecting updates from server..."
socket_results.connect ("tcp://"+system_ip+":%s" % port)
topicfilter = "9"
print ("filter:",topicfilter)
socket_results.setsockopt(zmq.SUBSCRIBE, topicfilter)


def splitArray(A,B,n):
	a = np.array([row [0:n/2] for row in A[0:n/2]])
	b = np.array([row [n/2:n] for row in A[0:n/2]])
	c = np.array([row [0:n/2] for row in A[n/2:n]])
	d = np.array([row [n/2:n] for row in A[n/2:n]])
	e = np.array([row [0:n/2] for row in B[0:n/2]])
	f = np.array([row [n/2:n] for row in B[0:n/2]])
	g = np.array([row [0:n/2] for row in B[n/2:n]])
	h = np.array([row [n/2:n] for row in B[n/2:n]])
	msg1 = modules.arr2str(np.concatenate((a,e,b,g,np.array([[1]*(n/2)])),axis=0))
	msg2 = modules.arr2str(np.concatenate((a,f,b,h,np.array([[2]*(n/2)])),axis=0))
	msg3 = modules.arr2str(np.concatenate((c,e,d,g,np.array([[3]*(n/2)])),axis=0))
	msg4 = modules.arr2str(np.concatenate((c,f,d,h,np.array([[4]*(n/2)])),axis=0))
	return [msg1, msg2, msg3, msg4]

def combine (A) :
	a =  A[1]
	b =  A[2] 
	c = A[3]
	d= A[4]
	p= np.concatenate( (a,b), axis =1 ) 
	q= np.concatenate( (c,d), axis =1 ) 
	result = np.concatenate( (p,q), axis =0 )
	return result

def compileResult(VMs):
	parts = 0
	ans = 0
	msgs = []
	arrays = {}
	time.sleep(0.2)

	while parts < VMs:
		try:
			print "Getting Query.."
			string = socket_results.recv()
			messagedata = string[2:]
			resp = str(messagedata)
			print "Appending:",modules.str2arr(resp)
			msgs.append(resp)
			parts += 1
		except:
			print("Waiting for Result in Queue qresult")
	print("\nParts recieved: %d" % (len(msgs)))
	print modules.str2arr(msgs[0])
	print modules.str2arr(msgs[1])
	print modules.str2arr(msgs[2])
	print modules.str2arr(msgs[3])
	for msg in msgs:
		msg = modules.str2arr(msg)
		arrays[msg[-1][0]] = msg[:-1]
	print arrays
	print combine(arrays)



def distributeQuery(N, VMs=4):
	start_time = time.time()
	A = np.reshape(np.arange(N*N),(N,N))
	msgs = splitArray(A,A,N)
	for vm in range(VMs):
		print("Sending Query: quater(%s)"%(vm))
		socket.send("%d %s" % (vm, msgs[vm]))
    	time.sleep(0.1)
	time.sleep(0.5)
	compileResult(VMs)


inp = raw_input("Distributed Algorithm to perform matrix multiplication\nEnter the value of N for the Matrix NxN:\n")
n = int(inp)
print "Entered:",n
distributeQuery(n, 4)