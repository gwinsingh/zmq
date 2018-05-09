import zmq
import random
import sys
import time

port = "5559"
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.connect("tcp://localhost:%s" % port)
publisher_id = random.randrange(0,9999)
while True:
    topic = 9
    messagedata = "server#%s" % publisher_id
    print "%s %s" % (topic, str(publisher_id))
    socket.send("%d %s" % (topic, str(publisher_id)))
    time.sleep(2)
