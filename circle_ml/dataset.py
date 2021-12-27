import os
import json

import torch
import math
import random
import numpy as np
import torch.nn.functional as F
from torch.utils import data
from torch.utils.data import Dataset
from torch.nn.utils.rnn import pad_sequence


class CircleDataset(Dataset):
    def __init__(self, data_list, augmentation = True):
        self.augmentation = augmentation
        self.data = data_list

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        data_array, label = self.data[index]

        if self.augmentation:
            rand_len = random.randint(20, 80)
            if data_array.shape[0] > rand_len:
                del_len = data_array.shape[0] - rand_len
                for _ in range(del_len):
                    rand_row = random.randint(0, data_array.shape[0] - 1)
                    data_array = np.delete(data_array, rand_row, 0)
            elif data_array.shape[0] < rand_len:
                insert_len = rand_len - data_array.shape[0]
                for _ in range(insert_len):
                    rand_num = random.randint(0, data_array.shape[0] - 1)
                    rand_row = data_array[rand_num]
                    data_array = np.insert(data_array, rand_num, rand_row, 0)

        data_array = torch.from_numpy(data_array)
        return torch.FloatTensor(data_array), torch.tensor(label)


def get_data(data_dir):
    data_list = []
    for label_dir in os.listdir(data_dir):
        label_path = os.path.join(data_dir, label_dir)
        for data in sorted(os.listdir(label_path)):
            data_path = os.path.join(label_path, data)
            data_array = np.load(data_path)
            data_array = data_array.astype(np.float32)
            if label_dir.endswith('forward'):
                data_list.append((data_array, 0))
            elif label_dir.endswith('backward'):
                data_list.append((data_array, 1))
            elif label_dir.endswith('others'):
                data_list.append((data_array, 2))
            else:
                print(f"we got {label_dir} in label dir")
    return data_list


def collate_batch(batch):
    # Process features within a batch.
    """Collate a batch of data."""
    data_seq, label = zip(*batch)
    # Because we train the model batch by batch, we need to pad the features in the same batch to make their lengths the same.
    data_seq = pad_sequence(data_seq, batch_first=True, padding_value=-20)    # pad log 10^(-20) which is very small value.
    # mel: (batch size, length, 40)
    label = list(label)
    label = torch.cat(
        [label[i].unsqueeze(0) for i in range(len(label))],
        dim=0,
    )
    return data_seq, label