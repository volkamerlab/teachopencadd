# Data

This folder stores input and output data for the Jupyter notebook.

For **input** we have, `CHEMBL25_activities_EGFR.csv` which is the training dataset used to train the neural network model and `test.csv` is the unknown dataset which is used to predict the target values for the unknown compounds using our trained model.  

For **output** we have, `best_weights.hdf5` file which stores the best weights after the model is trained and `ANN_model.hdf5` file is the saved neural network model. 
`predicted_pIC50_df` is the csv file containing the predicted pIC50 values for unknown dataset using the trained neural network model.
