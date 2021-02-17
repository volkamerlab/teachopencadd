# Data

This folder stores input and output data for the Jupyter notebook.

As input files, we have:

- `CHEMBL25_activities_EGFR.csv`: the dataset used to train the neural network.
- `test.csv`: the unlabeled dataset. It contains compounds for which we will provide pIC50 predictions, using the trained neural network.

As output files, we have:
- `best_weights.hdf5`: which stores the best weights after the neural network is trained.
- `ANN_model.hdf5`: the artificial neural network (ANN) saved for reproducibility of results.
- `predicted_pIC50_df.csv`: the csv file containing the predicted pIC50 values for the compounds in the `test.csv` dataset using the trained neural network.
