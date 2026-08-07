import torch 
import numpy as np


def train_loop(model, opt, loss_fn, dataloader, device):
    """
    Method from "A detailed guide to Pytorch's nn.Transformer() module.", by
    Daniel Melchor: https://medium.com/@danielmelchor/a-detailed-guide-to-pytorchs-nn-transformer-module-c80afbc9ffb1
    """
    
    model.train()
    total_loss = 0
    # total_acc = 0
    # total = 0
    
    for batch in dataloader:
        X, y = batch[:, 0], batch[:, 1]
        # X = np.vstack(X).astype(np.int64)
        X = np.array([arr.astype(np.int64) for arr in X])
        X, y = torch.tensor(X).to(device), torch.tensor(y.astype(np.float32)).to(device)

        # Now we shift the tgt by one so with the <SOS> we predict the token at pos 1
        # y_input = y[:,:-1]
        # y_expected = y[:,1:]
        
        # Get mask to mask out the next words
        # sequence_length = y_input.size(1)
        # tgt_mask = model.get_tgt_mask(sequence_length).to(device)

        # Standard training except we pass in y_input and tgt_mask
        pred = model(X) # y_input, tgt_mask)

        # Permute pred to have batch size first again
        # pred = pred.permute(1, 2, 0)      
        loss = loss_fn(pred, y.float().unsqueeze(1)) # y_expected)

        # correct = pred.argmax(axis=1) == y 

        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 0.5)
        opt.step()
    
        total_loss += loss.detach().item()
        # total_acc += correct.sum().item()
        # total += correct.size(0)
        
    return total_loss / len(dataloader)# , total_acc / total 


def validation_loop(model, loss_fn, dataloader, device):
    """
    Method from "A detailed guide to Pytorch's nn.Transformer() module.", by
    Daniel Melchor: https://medium.com/@danielmelchor/a-detailed-guide-to-pytorchs-nn-transformer-module-c80afbc9ffb1
    """
    
    model.eval()
    total_loss = 0
    # total_acc = 0
    # total = 0
    
    with torch.no_grad():
        for batch in dataloader:
            X, y = batch[:, 0], batch[:, 1]
            X = np.vstack(X).astype(np.int64)
            X, y = torch.tensor(X).to(device), torch.tensor(y.astype(np.float32)).to(device)
            # Now we shift the tgt by one so with the <SOS> we predict the token at pos 1
            # y_input = y[:,:-1]
            # y_expected = y[:,1:]
            
            # Get mask to mask out the next words
            # sequence_length = y_input.size(1)
            # tgt_mask = model.get_tgt_mask(sequence_length).to(device)

            # Standard training except we pass in y_input and src_mask
            pred = model(X) #y_input, tgt_mask)

            # Permute pred to have batch size first again
            # pred = pred.permute(1, 2, 0)      
            loss = loss_fn(pred, y.unsqueeze(1)) #y_expected)
            # correct = pred.argmax(axis=1) == y 
            total_loss += loss.detach().item()
            # total_acc += correct.sum().item()
            # total += correct.size(0)
        
    return total_loss / len(dataloader)# , total_acc / total


def fit(model, opt, loss_fn, train_dataloader, val_dataloader, epochs, device):
    """
    Method from "A detailed guide to Pytorch's nn.Transformer() module.", by
    Daniel Melchor: https://medium.com/@danielmelchor/a-detailed-guide-to-pytorchs-nn-transformer-module-c80afbc9ffb1
    """
    
    # Used for plotting later on
    train_loss_list, validation_loss_list = [], []
    
    print("Training and validating model")
    for epoch in range(epochs):
        print("-"*25, f"Epoch {epoch + 1}","-"*25)
        
        train_loss = train_loop(model, opt, loss_fn, train_dataloader, device)
        train_loss_list += [train_loss]
        #train_acc_list += [train_acc]
        
        validation_loss = validation_loop(model, loss_fn, val_dataloader, device)
        validation_loss_list += [validation_loss]
        #validation_acc_list += [validation_acc]
        
        print(f"Training loss: {train_loss:.4f}")
        #print(f"Training accuracy: {train_acc:.4f}")
        print(f"Validation loss: {validation_loss:.4f}")
        #print(f"Validation accuracy: {validation_acc:.4f}")
        print()
        
    return train_loss_list, validation_loss_list# , train_acc_list, validation_acc_list
    
