import os
import json

import torch
import math
import random
import numpy as np
import torch.nn.functional as F
from torch.utils import data
from torch.utils.data import Dataset


class CircleDataset(Dataset):
    def __init__(self, data_dir):
        self.data_dir = data_dir

        self.data = self.get_data(data_dir)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        data_array, label = self.data[index]
        data_array.dtype = 'float'
        data_array = torch.from_numpy(data_array)
        return torch.tensor(data_array), torch.tensor(label)

    def get_data(self, data_dir):
        data_list = []
        for label_dir in os.listdir(data_dir):
            label_path = os.path.join(data_dir, label_dir)
            for data in sorted(os.listdir(label_path)):
                data_path = os.path.join(label_path, data)
                data_array = np.load(data_path)
                if label_dir.endswith('forward'):
                    data_list.append((data_array, 0))
                elif label_dir.endswith('backward'):
                    data_list.append((data_array, 1))
                elif label_dir.endswith('others'):
                    data_list.append((data_array, 2))
                else:
                    print(f"we got {label_dir} in label dir")
        return data_list
