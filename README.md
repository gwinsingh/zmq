# zmq
Distributed Matriz Multiplication over network using ZeroMQ Python

The file `slave.py` is supposed to perform all the computation. By default 4 instances of `slave.py` need to be run.
The `master.py` passes on the data to be computed to the running `slave.py` instances.

Prerequisites:
1. numpy:
>> sudo pip install numpy

2. zmq:
>> sudo pip install pyzmq-static


Instructions:

1. Initiate the apprpritate value of teh variable "system_ip" in files `slave.py` and `master.py`
2. Run the forwarding servers:
>> python forwarder_device.py &
>> python forwarder_device2.py &
3. Run the Slave instances on same or different VMs:
>> python slave.py 0
>> python slave.py 1
>> python slave.py 2
>> python slave.py 3
4. Run the Master instance:
>> python master.py

