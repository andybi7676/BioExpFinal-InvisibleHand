# -*- coding: utf-8 -*-

import os
import random
import torch
import math
import argparse
import torch.nn as nn
import numpy as np

from multiprocessing import cpu_count
from tqdm import tqdm
from torch.optim import AdamW
from torch.utils.data import Dataset, DataLoader, random_split
from tensorboardX import SummaryWriter 
 

from dataset import CircleDataset, get_data
from model import ResNetClassifier


def get_dataloader(data_dir, batch_size, n_workers):
    """Generate dataloader"""

    # Split dataset into training dataset and validation dataset
    data_list = get_data(data_dir)
    valid_data = random.sample(data_list, k=int(0.1 * len(data_list)))
    train_data = data_list
    for data in valid_data:
        for i in range(len(train_data)):
            if np.all(train_data[i][0] == data[0]):
                train_data.remove(train_data[i])
                break
    
    trainset = CircleDataset(train_data)
    validset = CircleDataset(valid_data, augmentation=False)
    train_loader = DataLoader(
        trainset,
        batch_size=batch_size,
        shuffle=True,
        drop_last=True,
        num_workers=n_workers,
        pin_memory=True,
        collate_fn=None,
    )
    valid_loader = DataLoader(
        validset,
        batch_size=1,
        num_workers=n_workers,
        drop_last=True,
        pin_memory=True,
        collate_fn=None,
    )

    return train_loader, valid_loader


"""# Model Function
- Model forward function.
"""

def model_fn(batch, model, criterion, device):
    """Forward a batch through the model."""

    data, labels = batch
    data = data.to(device)
    labels = labels.to(device)

    outs = model(data)
    loss = criterion(outs, labels)

    return loss, outs, labels


"""# Validate
- Calculate accuracy of the validation set.
"""

def valid(dataloader, model, criterion, device): 
    """Validate on validation set."""

    model.eval()
    running_loss = 0.0
    pbar = tqdm(total=len(dataloader.dataset), ncols=0, desc="Valid", unit=" uttr")

    accuracy = 0
    for i, batch in enumerate(dataloader):
        with torch.no_grad():
            loss, outs, labels = model_fn(batch, model, criterion, device)
            running_loss += loss.item()
            preds = outs.argmax(dim=-1).cpu().numpy()
            for pred, label in zip(preds, labels):
                if pred == label:
                    accuracy += 1

        pbar.update(dataloader.batch_size)
        pbar.set_postfix(
        loss=f"{running_loss / (i+1):.2f}",
        )

    pbar.close()
    model.train()
    accuracy /= len(dataloader)
    print(f"[Info]: We got accuracy {accuracy} in {len(dataloader)} sequences!",flush = True) 

    return running_loss / len(dataloader)


"""# Main function"""


def main(
    data_dir,
    out_dir,
    batch_size,
    n_workers,
    epochs,
):
    """Main function."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[Info]: Use {device} now!")

    train_loader, valid_loader = get_dataloader(data_dir, batch_size, n_workers)
    train_iterator = iter(train_loader)
    print(f"[Info]: Finish loading data!",flush = True)

    valid_steps = len(train_loader)
    save_steps = valid_steps
    total_steps = valid_steps * epochs
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
    ckpt_file = os.path.join(out_dir, "resnet.ckpt")
    if os.path.isfile(ckpt_file):
        model.load_state_dict(torch.load(ckpt_file))
        print("[Info]: Load model checkpoint!",flush = True)
    criterion = nn.CrossEntropyLoss().to(device)
    optimizer = AdamW(model.parameters(), lr=1e-3)
    scheduler = torch.optim.lr_scheduler.StepLR(
       optimizer, step_size = valid_steps * 50, gamma = 0.5)
    print(f"[Info]: Finish creating model!",flush = True)

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    writer = SummaryWriter(out_dir)

    best_loss = 10000000
    best_state_dict = None

    pbar = tqdm(total=valid_steps, ncols=0, desc="Train", unit=" step")

    for step in range(total_steps):    
        # Get data
        try:
            batch = next(train_iterator)
        except StopIteration:
            train_iterator = iter(train_loader)
            batch = next(train_iterator)

        loss, _, _ = model_fn(batch, model, criterion, device)
        batch_loss = loss.item()
        writer.add_scalar('training_loss', loss, step)

        # Update model
        loss.backward()
        optimizer.step()
        scheduler.step()
        optimizer.zero_grad()
        
        # Log
        pbar.update()
        pbar.set_postfix(
        loss=f"{batch_loss:.2f}",
        step=step + 1,
        )

        # Do validation
        if (step + 1) % valid_steps == 0:
            pbar.close()

            valid_loss = valid(valid_loader, model, criterion, device)
            writer.add_scalar('valid_loss', valid_loss, step)

            # keep the best model
            if valid_loss < best_loss:
                best_loss = valid_loss
                best_state_dict = model.state_dict()

            pbar = tqdm(total=valid_steps, ncols=0, desc="Train", unit=" step")
            print(f"\n[Info]: Current lr:{optimizer.param_groups[0]['lr']}", flush = True)

        # Save the best model so far.
        if (step + 1) % save_steps == 0 and best_state_dict is not None:
            save_path = os.path.join(out_dir, "resnet.ckpt")
            torch.save(best_state_dict, save_path)
            pbar.write(f"Step {step + 1}, best model saved. (loss={best_loss:.4f})")

    pbar.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='configs for training')  
    parser.add_argument('--data_dir', '-d', metavar='DATA',
                        default='data', help='The dataset folder')
    parser.add_argument('--out_dir', '-o', metavar='OUT', default='./results',
                        help='Output directory')
    parser.add_argument('--n_workers', '-n', metavar='N', type=int,
                        default=cpu_count()-1,
                        help='The number of worker threads for preprocessing')
    parser.add_argument('--batch_size', '-b', metavar='BATCH', type=int,
                        default=1,  help='training batch size')
    parser.add_argument('--epochs', '-e', metavar='VALID', type=int,
                        default=100,  help='training segment length')
    args = parser.parse_args()
    main(**vars(args))
