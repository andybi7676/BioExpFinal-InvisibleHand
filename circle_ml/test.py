# -*- coding: utf-8 -*-

import os
import argparse

import torch
import numpy as np
from torch.utils.data import DataLoader
from tqdm.notebook import tqdm
from multiprocessing import cpu_count

from dataset import CircleDataset
from model import ResNetClassifier


def main(
    data_dir,
    out_dir,
    num_workers,
):
    """Main function."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[Info]: Use {device} now!")

    data_dir = os.path.abspath(data_dir)
    dataset = CircleDataset(data_dir)
    dataloader = DataLoader(
        dataset,
        batch_size=1,
        shuffle=False,
        drop_last=False,
        num_workers=num_workers,
        collate_fn=None,
    )
    print(f"[Info]: Finish loading data!",flush = True)

    model = ResNetClassifier(
        label_num=3,
        in_channels=[6, 16, 16],
        out_channels=[16, 16, 8],
        downsample_scales=[1, 1, 1],
        kernel_size=3,
        z_channels=8,
        dilation=True,
        leaky_relu=True,
        dropout=0.0,
        stack_kernel_size=3,
        stack_layers=2,
        nin_layers=0,
        stacks=[3, 3, 3],
    ).to(device)
    model_path = os.path.join(out_dir, 'resnet.ckpt')
    model.load_state_dict(torch.load(model_path))
    model.eval()
    print(f"[Info]: Finish creating model!",flush = True)

    data_len = len(dataloader)
    accuracy = 0
    for data, labels in tqdm(dataloader):
        with torch.no_grad():
            data = data.to(device)
            labels = labels.to(device)
            preds = model(data)
            preds = preds.cpu().numpy()
            for pred, label in zip(preds, labels):
                if pred == label:
                    accuracy += 1

    accuracy /= data_len
    print(f"[Info]: We got accuracy {accuracy} in {data_len} sequences!",flush = True) 
  


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='configs for training')  
    parser.add_argument('--data_dir', '-d', metavar='DATA',
                        default='data', help='The dataset folder')
    parser.add_argument('--out_dir', '-o', metavar='OUT', default='./results',
                        help='Output directory')
    parser.add_argument('--num_workers', '-n', metavar='N', type=int,
                        default=cpu_count()-1,
                        help='The number of worker threads for preprocessing')
    args = parser.parse_args()
    main(**vars(args))