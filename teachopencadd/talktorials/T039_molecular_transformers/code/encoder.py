import torch 
import torch.nn as nn
import math 


class PositionalEncoding(nn.Module):
    def __init__(self, dim_model, dropout_p, max_len):
        super().__init__()
        # Modified version from: https://pytorch.org/tutorials/beginner/transformer_tutorial.html
        # max_len determines how far the position can have an effect on a token (window)
        
        # Info
        self.dropout = nn.Dropout(dropout_p)
        
        # Encoding - From formula
        pos_encoding = torch.zeros(max_len, 1, dim_model)
        # positions_list = torch.arange(0, max_len, dtype=torch.float).view(-1, 1) # 0, 1, 2, 3, 4, 5
        # positions_list = torch.arange(max_len).unsqueeze(1)
        # division_term = torch.exp(torch.arange(0, dim_model, 2) * (-math.log(10000.0) / dim_model))

        # division_term = torch.exp(torch.arange(0, dim_model, 2).float() * (-math.log(10000.0)) / dim_model) # 1000^(2i/dim_model)
        factor = -math.log(10000.0) / dim_model  # outs loop
        for pos in range(0, max_len):  # position of word in seq
            for i in range(0, dim_model, 2):  # pos of embed of word
                div_term = math.exp(i * factor)
                pos_encoding[pos, 0, i] = math.sin(pos * div_term)
                pos_encoding[pos, 0, i+1] = math.cos(pos * div_term)
        # PE(pos, 2i) = sin(pos/1000^(2i/dim_model))
        # pos_encoding[:, 0, 0::2] = torch.sin(positions_list * division_term)
        
        # PE(pos, 2i + 1) = cos(pos/1000^(2i/dim_model))
        # pos_encoding[:, 0, 1::2] = torch.cos(positions_list * division_term)
        
        # Saving buffer (same as parameter without gradients needed)
        # pos_encoding = pos_encoding.unsqueeze(0).transpose(0, 1)
        self.register_buffer("pos_encoding", pos_encoding)
        
    def forward(self, token_embedding: torch.tensor) -> torch.tensor:
        # Residual connection + pos encoding
        pos_enc = self.pos_encoding[:token_embedding.size(0), :]
        token_embedding = token_embedding + pos_enc
        return self.dropout(token_embedding)