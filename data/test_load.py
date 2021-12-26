import os
import glob
import numpy as np

file_name = './raw_data/forward/forward-10.npy'

data = np.load(file_name)
print(data)