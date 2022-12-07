"""
This code is adapted from talktorial 022.
"""

import numpy as np
import pandas as pd

from rdkit import Chem
from rdkit.Chem import MACCSkeys
from rdkit.Chem.rdMolDescriptors import GetMorganFingerprintAsBitVect

# Neural network specific libraries
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import ModelCheckpoint


def neural_network_model(layer_sizes):
    """
    Creating a neural network from two hidden layers
    using ReLU as activation function in the two hidden layers
    and a linear activation in the output layer.

    Parameters
    ----------
    layer_sizes : List[int]
        Width of linear layers.

    Returns
    -------
    model
        Fully connected neural network model with two hidden layers.
    """

    model = Sequential()
    # First hidden layer
    for i, width in enumerate(layer_sizes):
        model.add(Dense(width, activation="relu", name=f"layer{i}"))
    # Output layer
    model.add(Dense(1, activation="linear", name="output"))

    # Compile model
    model.compile(loss="mean_squared_error", optimizer="adam", metrics=["mse", "mae"])
    return model


def create_and_fit_model(x_train, y_train, x_test, y_test, layers=[512, 128, 64], **kwargs):
    """
    Create and fit an instance of a feed-forward neural network (see Talktorial 022).
    
    Parameters
    ----------
    layers: List[int]
        The width of hidden layers in the feed-forward neural net.
    
    **kwargs
        The keyword arguments are passed to the `model.fit` function.
    
    Returns
    -------
    Sequential
        A fitted feed-forward NN.
    """
    model = neural_network_model(layers)
    # Fit model on x_train, y_train data
    history = model.fit(
        np.array(list((x_train))).astype(float),
        y_train,
        validation_data=(np.array(list((x_test))).astype(float), y_test),
        **kwargs,
    )
    
    return model


def smiles_to_fp(smiles, method="maccs", n_bits=2048):
    """
    Encode a molecule from a SMILES string into a fingerprint.

    Parameters
    ----------
    smiles : str
        The SMILES string defining the molecule.

    method : str
        The type of fingerprint to use. Default is MACCS keys.

    n_bits : int
        The length of the fingerprint.

    Returns
    -------
    array
        The fingerprint array.
    """

    # Convert smiles to RDKit mol object
    mol = Chem.MolFromSmiles(smiles)

    if method == "maccs":
        return np.array(MACCSkeys.GenMACCSKeys(mol))
    if method == "morgan2":
        return np.array(GetMorganFingerprintAsBitVect(mol, 2, nBits=n_bits))
    if method == "morgan3":
        return np.array(GetMorganFingerprintAsBitVect(mol, 3, nBits=n_bits))
    else:
        print(f"Warning: Wrong method specified: {method}." " Default will be used instead.")
        return np.array(MACCSkeys.GenMACCSKeys(mol))


def load_chembl_egfr_data(data_dir, **kwargs):
    """
    Load the CHEMBL25 activities as in T022 and compute fingerprints for each entry. The fingerprints are
    created by `smiles_to_fp` to which `**kwargs` are passed.
    
    Parameters
    ----------
    data_dir : Path
        The absolute data directory to the CHEMBL EGFR activities.
        
    **kwargs :
        The keyword arguments are passed to the fingerprint function.
    
    Returns
    -------
    pandas.DataFrame
        The dataframe containing `fingerprints_df` and the target `pIC50`.
    """
    # Load data
    df = pd.read_csv(data_dir, index_col=0)
    df = df.reset_index(drop=True)
    # Keep necessary columns
    df = df[df["units"] == "nM"]
    chembl_df = df[["canonical_smiles", "pIC50"]]
    chembl_df["fingerprints_df"] = chembl_df["canonical_smiles"].apply(smiles_to_fp, **kwargs)
    return chembl_df