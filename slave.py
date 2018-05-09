import time
import modules
import numpy as np
import sys
import zmq

port = "5560"
# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)
print "Collecting updates from server..."
socket.connect ("tcp://192.168.0.132:%s" % port)
topicfilter = sys.argv[1]
print ("filter:",topicfilter)
socket.setsockopt(zmq.SUBSCRIBE, topicfilter)


# context_results = zmq.Context()
# socket_results = context_results.socket(zmq.PUSH)
# ip = "192.168.56.1"
# socket_results.connect("tcp://"+ip+":5598")

port = "5659"
context_results = zmq.Context()
socket_results = context_results.socket(zmq.PUB)
socket_results.connect("tcp://192.168.0.132:%s" % port)

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
	# socket_results.send(modules.arr2str(answer))
	# modules.sendToQueue('qresult', modules.arr2str(answer))

while True:
	string = socket.recv()
	# print "\n"*3,string,"\n"*3
	# topic, messagedata = string.split()
	messagedata = string[2:]
	msg = messagedata
	processMessage(msg)

# def fetchMessage(queueName):
# 	sqs = boto3.resource('sqs')
# 	queue = sqs.get_queue_by_name(QueueName=queueName)
# 	client = boto3.client('sqs')

# 	# Get URL for SQS queue
# 	response = client.receive_message(
# 	    QueueUrl=queue.url,
# 	    MaxNumberOfMessages=1,
# 	)
# 	# print response
# 	try:
# 		messages = response['Messages']
# 		for msg in messages:
# 			body = msg['Body']
# 			print "Message Received: { %s } from Queue: { %s }" %(modules.str2arr(body), queueName)
# 			rhandle = msg['ReceiptHandle']
# 			del_response = client.delete_message(
# 			    QueueUrl=queue.url,
# 			    ReceiptHandle=rhandle
# 			)
# 			# print del_response
# 			return body
# 	except:
# 		return ""


# def listen():
# 	while True:
# 		msg = fetchMessage('qinfo')
# 		if len(msg) == 0:
# 			print "Queue is empty"
# 			time.sleep(3)
# 		else:
# 			processMessage(msg)

# if __name__ == '__main__':
# 	fetchMessage('qinfo')
# 	listen()

