import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import numpy as np
# import urllib
import pickle

# load model
filename = "./models/first.pickle"
model = pickle.load(open(filename, "rb"))

predicted = model.predict(np.array([484, 50, 450.0, 50, 10.0, 40]).reshape(1, -1))

print(predicted)