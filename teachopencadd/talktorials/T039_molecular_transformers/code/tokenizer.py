import re 
from collections import Counter 


class SmilesTokenizer(object):
    """
    A simple regex-based tokenizer adapted from the deepchem smiles_tokenizer package.
    SMILES regex pattern for the tokenization is designed by Schwaller et. al., ACS Cent. Sci 5 (2019)
    """

    def __init__(self):
        self.regex_pattern = (
            r"(\[[^\]]+]|Br?|Cl?|N|O|S|P|F|I|b|c|n|o|s|p|\(|\)|\."
            r"|=|#|-|\+|\\|\/|:|~|@|\?|>>?|\*|\$|\%[0-9]{2}|[0-9])"
        )
        self.regex = re.compile(self.regex_pattern)

    def tokenize(self, smiles):
        """
        Tokenizes SMILES string.

        Parameters
        ----------
        smiles : str
            Input SMILES string.

        Returns
        -------
        List[str]
            A list of tokens.
        """
        tokens = [token for token in self.regex.findall(smiles)]
        return tokens
    
def build_vocab(smiles_list, tokenizer, max_vocab_size):
    """
    Builds a vocabulary of N=max_vocab_size most common tokens from list of SMILES strings.

    Parameters
    ----------
    smiles_list : List[str]
        List of SMILES strings.
    tokenizer : SmilesTokenizer
    max_vocab_size : int
        Maximum size of vocabulary.

    Returns
    -------
    Dict[str, int]
        A dictionary that defines mapping of a token to its index in the vocabulary.
    """
    tokenized_smiles = [tokenizer.tokenize(s) for s in smiles_list]
    token_counter = Counter(c for s in tokenized_smiles for c in s)
    tokens = [token for token, _ in token_counter.most_common(max_vocab_size)]
    vocab = {token: idx for idx, token in enumerate(tokens)}
    return vocab


def smiles_to_ohe(smiles, tokenizer, vocab):
    """
    Transforms SMILES string to one-hot encoding representation.

    Parameters
    ----------
    smiles : str
        Input SMILES string.
    tokenizer : SmilesTokenizer
    vocab : Dict[str, int]
        A dictionary that defines mapping of a token to its index in the vocabulary.

    Returns
    -------
    Tensor
        A pytorch Tensor with shape (n_tokens, vocab_size), where n_tokens is the
        length of tokenized input string, vocab_size is the number of tokens in
        the vocabulary
    """
    unknown_token_id = len(vocab) - 1
    token_ids = [vocab.get(token, unknown_token_id) for token in tokenizer.tokenize(smiles)]
    # ohe = torch.eye(len(vocab))[token_ids]
    return token_ids # ohe