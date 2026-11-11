import numpy as np 
from torch.nn.utils.rnn import pad_sequence

import random 
import tokenizer
import math 
import torch 


def generate_random_data(n):
    SOS_token = np.array([2])
    EOS_token = np.array([3])
    length = 8

    data = []

    # 1,1,1,1,1,1 -> 1,1,1,1,1
    for i in range(n // 3):
        X = np.concatenate((SOS_token, np.ones(length), EOS_token))
        y = 1 # np.concatenate((SOS_token, np.ones(length), EOS_token))
        data.append([X, y])

    # 0,0,0,0 -> 0,0,0,0
    for i in range(n // 3):
        X = np.concatenate((SOS_token, np.zeros(length), EOS_token))
        y = 0 # np.concatenate((SOS_token, np.zeros(length), EOS_token))
        data.append([X, y])

    # 1,0,1,0 -> 1,0,1,0,1
    for i in range(n // 3):
        X = np.zeros(length)
        start = random.randint(0, 1)

        X[start::2] = 1

        # y = np.zeros(length)
        #if X[-1] == 0:
        #    y[::2] = 1
        #else:
        #    y[1::2] = 1

        X = np.concatenate((SOS_token, X, EOS_token))
        y = 1 # np.concatenate((SOS_token, y, EOS_token))

        data.append([X, y])

    np.random.shuffle(data)

    return data


def batchify_data(data, batch_size=64, padding=True, padding_token=30):
    batches = []
    for idx in range(0, len(data), batch_size):
        # We make sure we dont get the last bit if its not batch_size size
        if idx + batch_size < len(data):
            # Here you would need to get the max length of the batch,
            # and normalize the length with the PAD token.
            if padding:
                max_batch_length = 0

                # Get longest sentence in batch
                for seq in data[idx : idx + batch_size]:
                    if len(seq[0]) > max_batch_length:
                        max_batch_length = len(seq[0])
                # Append X padding tokens until it reaches the max length
                for seq_idx in range(batch_size):
                   remaining_length = max_batch_length - len(data[idx + seq_idx][0])
                   data[idx + seq_idx][0] = np.concatenate([data[idx + seq_idx][0], np.array([padding_token] * remaining_length, dtype=np.int64)], axis=0)
            batches.append(np.array(data[idx : idx + batch_size]))

    print(f"{len(batches)} batches of size {batch_size}")
    # batches = add_padding(batches)
    return batches


def generate_dataset(smiles, y, token, vocab): 
    # data = np.array(zip(smiles, y))
    # build a vocab using the training data

    data = []
    smiles = [tokenizer.smiles_to_ohe(smi, token, vocab) for smi in smiles]
    for smi, tar in zip(smiles, y): 
        if not math.isnan(tar): 
            smi = np.array(smi)
            # smi = np.concatenate((SOS_token, smi, EOS_token))
            data.append([smi, tar])

    np.random.shuffle(data)
    return data

def add_padding(data): 
    data = pad_sequence(sequences=torch.tensor(data),
        batch_first=True,
        padding_value=0,
    )
    return data