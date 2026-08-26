# Inductive Conformal Prediction


Traditional machine learning models output a point value (regression) or class (classification) but do not provide rigorous guarantees about uncertainty.

Inductive conformal prediction (CP) addresses this limitation by transforming model outputs into prediction intervals (regression) or sets (classification) with statistical coverage guarantees. For a chosen confidence level (e.g. 95%), CP guarantees that the true label will be contained in the prediction set at least 95% of the time, assuming data sets are exchangeable (*marginal coverage guarantee*). Exchangability is a weaker assumption than independent and identically distributed (i.i.d.) data, which is typically assumed in machine learning.

The theoretical part of the notebook is based on [this publication](https://arxiv.org/abs/2107.07511). For more in-depth explanation, we refer the reder therefore to Angelopoulos and Bates.

In this notebook we:

1. Generate molecular descriptors from SMILES structures.
2. Train a Random Forest classifier.
3. Calibrate the model using a separate calibration dataset.
4. Compute non-conformity scores.
5. Construct conformal prediction sets.
6. Evaluate how uncertainty changes the interpretation of model predictions.


The dataset contains molecular structures represented as SMILES strings. These structures are converted into numerical molecular descriptors which serve as input features for machine learning.


### Molecular Descriptor Generation

Most machine learning algorithms cannot directly process molecular structures.
We therefore convert each molecule into a vector of physicochemical properties
using RDKit.

Examples include:

- Molecular weight
- Topological indices
- Electrotopological descriptors
- Ring counts
- Functional group counts

The resulting feature matrix contains over 200 descriptors per compound.


### Dataset Splitting

Inductive CP requires three distinct datasets:

- Training set:
  used to fit the machine learning model

- Calibration set:
  used to estimate uncertainty and compute thresholds

- Test set:
  used only for final evaluation

Separating calibration from training is the key distinction between
inductive conformal prediction and standard model evaluation.


### Random Forest Classifier

A Random Forest is an ensemble method that combines many decision trees.

Advantages:

- Handles high-dimensional descriptor spaces well.
- Captures nonlinear relationships.
- Robust to noisy descriptors.
- Provides class probabilities that can be used by conformal prediction.

The model is trained only on the training set.


### Calibration

After training, predictions are generated for the calibration dataset.

For every calibration sample we compute a (non-)conformity score
that measures how compatible the observed class is with the model prediction. In our case, we compute a non-conformity score, which is called true class ($TC$) score, and that measures the probability of being wrong for a particular sample.

These non-conformity scores form an empirical reference distribution.

The conformal threshold ($\hat{q}$) is derived from a quantile of this distribution
and determines how prediction sets are constructed for unseen compounds.


#### Intuition behind the CP Sets

The RF produces a probability for each class. Rather than directly using these probabilities as confidence estimates, we define a *non-conformity score* as the probability that a prediction is wrong.

For a given sample \(x_i\), the non-conformity score is based on the true class $c_i$ and its corresponding prediction probability \(P(c_i)\)

$TC({x_i}) = 1 - P(c_i)$


A low score corresponds to being correct with a high probabiliyt, while a high score means that the model was wrong with a high probability.

During calibration, we determine a threshold ($\hat{q}$) corresponding to the maximum probability of being wrong that can be tolerated, while still achieving the desired coverage guarantee. This threshold is estimated from the calibration set and represents the largest non-conformity score that is acceptable for a prediction to be considered reliable.


### Test predictions

For a new compound, we construct the conformal prediction set by including every class whose non-conformity score is below this threshold:

$\{ c : 1-P(c) \le \hat{q} \}$

Intuitively, this means:

- Classes with a sufficiently low probability of being wrong are retained.
- Classes with a probability of being wrong that exceeds the calibrated threshold are excluded.
- If only one class satisfies the criterion, a singleton prediction set is produced.
- If multiple classes satisfy the criterion, the model expresses uncertainty by returning all plausible classes.
- In rare cases no class may satisfy the criterion, resulting in an empty prediction set.

The threshold is chosen such that, on average, the true class will be retained in the prediction set with at least the specified coverage level (e.g. 95%). Therefore, conformal prediction does not aim to identify the single most likely class. Instead, it identifies all classes whose probability of being wrong is sufficiently small to maintain the desired statistical guarantee.


As we consider binary classification, prediction sets can have three outcomes:

- Size 0 (only possible if $\hat{q} < 0.5$):
  insufficient support

- Size 1:
  confident prediction

- Size 2 only possible if $\hat{q} >= 0.5$):
  ambiguous prediction; both classes remain plausible

The more single-class sets are output, i.e., prediction sets containing exactly one class, the more certain is the model and the more _efficient_ is the CP score.

#### Efficiency 
In classification, efficiency is commonly quantified as the fraction of single-class prediction sets over all predictions.

An efficient conformal predictor produces many single-class predictions, while still maintaining the desired ceratinty guarantee, i.e., _coverage_. Prediction sets containing multiple classes indicate uncertainty and are, therefore, less informative.


#### Coverage

Coverage measures the validity of the conformal predictor. A prediction is considered covered if the true class is contained within the conformal prediction set. For example, if the prediction set is [0, 1], both classes are considered plausible and the prediction is counted as covered regardless of the true outcome.

The empirical coverage is calculated as the proportion of test compounds whose true label is included in the corresponding conformal prediction set. For a conformal predictor with a minimal certainty level of 95%, the empirical coverage should be close to or above 95%, demonstrating that the uncertainty estimates are well calibrated.

High coverage indicates that the conformal prediction sets reliably contain the true class, while lower-than-expected coverage may suggest violations of the assumptions underlying conformal prediction or insufficient calibration data.


### Conclusions

The RF classifier provides probability estimates for binary classification.

Inductive CP converts these probabilities into statistically
valid prediction sets by calibrating uncertainty on an independent calibration set.

Benefits:

- Rigorous coverage guarantees.
- Explicit uncertainty quantification.
- Improved reliability compared with raw probabilities.

Limitations:

- Requires a dedicated calibration set.
- Larger uncertainty leads to less specific predictions.
- Not really suited for small datasets $\rightarrow$ transductive CP is needed

Overall, CP provides a practical framework for deploying trustworthy
machine learning models in cheminformatics applications.



