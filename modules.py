import numpy as np
import pickle
import json

def arr2str(arr):
	return pickle.dumps(arr)

def str2arr(arr):
	return pickle.loads(arr)

def sendToQueue(queueName='qinfo', message='test message'):	
	sqs = boto3.resource('sqs')
	# Get URL for SQS queue
	queue = sqs.get_queue_by_name(QueueName=queueName)
	# print queue.url
	response = queue.send_message(MessageBody=message)
	print("Message Sent: { %s } to Queue: { %s }"%(str2arr(message), queueName))

def purge_qr():
	sqs = boto3.resource('sqs')
	queue = sqs.get_queue_by_name(QueueName="qresult")
	queue.purge()