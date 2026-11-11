import torch 
import numpy as np 


def predict(model, input_sequence):
    """
    Method from "A detailed guide to Pytorch's nn.Transformer() module.", by
    Daniel Melchor: https://medium.com/@danielmelchor/a-detailed-guide-to-pytorchs-nn-transformer-module-c80afbc9ffb1
    """
    model.eval()
    
    # Get source mask
    # tgt_mask = model.get_tgt_mask(y_input.size(1)).to(device)
    
    pred = model(input_sequence)
    # pred = pred.argmax(axis=1)

    return pred
  

def test_loop(model, loss_fn, dataloader, device):
    
    total_loss = 0
    # total_acc = 0
    # total = 0
    prediction = np.empty((0))
    ground_truth = np.empty((0))
    model.eval()

    for batch in dataloader:
        with torch.no_grad():
            X, y = batch[:, 0], batch[:, 1]
            X = np.array([arr.astype(np.int64) for arr in X])
            X, y = torch.tensor(X).to(device), torch.tensor(y.astype(np.float32)).to(device)

            pred = model(X)
            loss = loss_fn(pred, y.float().unsqueeze(1))

            # correct = pred.argmax(axis=1) == y 
            total_loss += loss.detach().item()
            # total_acc += correct.sum().item()
            # total += correct.size(0)
            prediction = np.concatenate((prediction, pred.cpu().detach().numpy()[:, 0]))
            ground_truth = np.concatenate((ground_truth, y.cpu().detach().numpy()))
        
    return total_loss / len(dataloader), prediction, ground_truth# , total_acc / total 

