import torch 
import torch.nn as nn 

import transformer
import data
import inference 
import training 
import tokenizer
import plot 

from pathlib import Path 
import pandas as pd 
import os


HERE = Path(__file__).parent.resolve()
DATA = HERE / "data"

# load the dataset
df = pd.read_csv(os.path.join(DATA, "qm9.csv.gz"), compression="gzip")
df = df.sample(frac=1).reset_index(drop=True)

smiles = df["smiles"].tolist()
y = df["mu"] 



# smiles = [tokenizer.smiles_to_ohe(smi, token, vocab) for smi in smiles]
sample_size = len(y) # 50000
train_index = int(sample_size * 0.8)
test_index = train_index + int(sample_size * 0.1)

# normalize data 
y_mean = y[:train_index].mean()
y_std = y[:train_index].std()
y = (y - y_mean) / y_std


max_vocab_size = 30
token = tokenizer.SmilesTokenizer()
vocab = tokenizer.build_vocab(smiles[:sample_size], token, max_vocab_size)
vocab_size = len(vocab)

train_data = data.generate_dataset(smiles[:train_index], y[:train_index], token, vocab)
val_data = data.generate_dataset(smiles[train_index:test_index], y[train_index:test_index], token, vocab)
test_data = data.generate_dataset(smiles[test_index:sample_size], y[test_index:sample_size], token, vocab)

train_dataloader = data.batchify_data(train_data)
val_dataloader = data.batchify_data(val_data)
test_dataloader = data.batchify_data(test_data)


# device = "cuda" if torch.cuda.is_available() else "cpu"
device =  "mps" if torch.backends.mps.is_available and torch.backends.mps.is_built() else "cpu"
print(device)

model = transformer.Transformer(
    num_tokens=vocab_size, dim_model=100, num_heads=4, num_encoder_layers=3, dropout_p=0.2
).to(device)
opt = torch.optim.SGD(model.parameters(), lr=0.01)
# loss_fn = nn.CrossEntropyLoss()
loss_fn = nn.MSELoss()

train_loss_list, val_loss_list = training.fit(model, opt, loss_fn, train_dataloader, val_dataloader, 50, device)

plot.plot_loss(train_loss_list, val_loss_list)

test_loss, predictions, ground_truth = inference.test_loop(model, loss_fn, test_dataloader, device)
print(f"Test loss: {test_loss:.4f}")
plot.plot_targets(predictions, ground_truth)
