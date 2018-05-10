import numpy as np
import pickle
import json

def arr2str(arr):
	return pickle.dumps(arr)

def str2arr(arr):
	return pickle.loads(arr)
