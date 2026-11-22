# AI-Based Network Anomaly Detector

## Problem Statement
Traditional network security often uses rule-based detection. This project explores whether machine learning can identify unusual network connection records using the NSL-KDD benchmark dataset.

**Project scope:** This is a dataset-based student prototype. The Streamlit interface accepts manually entered connection details. It does not capture or monitor live network traffic.

## Dataset
- **Dataset:** NSL-KDD
- **Training file:** `KDDTrain+.txt` (125,973 records)
- **Test file:** `KDDTest+.txt` (22,544 records)
- **Features:** 41 connection attributes, plus attack type and difficulty level.
- **Binary labels:** `0 = normal`, `1 = attack`.

Place both dataset files in the **project root directory**, alongside the Python scripts. The scripts currently read the files directly from this location; they do not read from an `archive/` folder.

## Methods explored

### 1. Isolation Forest
An unsupervised anomaly-detection baseline. The current script fits and evaluates on the same training file, so its printed metrics should be treated as an exploratory training-set result, not as performance on unseen data.

### 2. Random Forest
A supervised classifier trained using the dataset's normal/attack labels. The repository includes a same-file random split experiment and a separate KDDTrain+/KDDTest+ evaluation.

### 3. Class balancing and feature importance
A second Random Forest experiment uses class balancing and 300 trees. Feature importance is printed to help inspect which input columns the model uses. Feature importance does not prove that a feature causes an attack.

## Repository files

| File | Purpose |
|---|---|
| `explore_data.py` | Loads and explores the training dataset. |
| `train_model.py` | Runs the Isolation Forest baseline. |
| `train_supervised.py` | Trains and evaluates a Random Forest using a random split of KDDTrain+. |
| `test_on_realdata.py` | Trains on KDDTrain+ and evaluates on KDDTest+. |
| `test_improved.py` | Tests a class-balanced Random Forest with 300 trees and prints feature importance. |
| `evaluate_model.py` | Runs a reproducible held-out evaluation and prints a confusion matrix, classification report, and unseen-category counts. |
| `save_model.py` | Trains the model used by the Streamlit demo and saves the model, encoders, and feature-column list. |
| `app.py` | Runs the manual-input Streamlit demonstration. |
| `model.pkl` | Saved Random Forest model used by the demo. |
| `encoders.pkl` | Saved encoders for the three categorical input columns. |
| `columns.pkl` | Feature-column order expected by the saved model. |
| `KDDTrain+.txt` | NSL-KDD training dataset. |
| `KDDTest+.txt` | NSL-KDD test dataset. |

## Requirements
Python 3.13 is the version recorded during development. Install the required packages:

```bash
pip install pandas scikit-learn streamlit joblib
```

## Run the project

Run commands from the project root, where the dataset files are stored.

```bash
python explore_data.py
python train_model.py
python train_supervised.py
python test_on_realdata.py
python test_improved.py
python evaluate_model.py
```

`evaluate_model.py` trains the 300-tree balanced Random Forest on KDDTrain+ and reports results on the separate KDDTest+ file, including a confusion matrix and counts of previously unseen categorical values.

To retrain and save the model files used by the Streamlit demo:

```bash
python save_model.py
```

After changing the preprocessing format, regenerate the saved model artifacts before opening the app. The existing committed `.pkl` files were created with the previous encoder and may be incompatible with the updated app.

To launch the manual-input demo:

```bash
streamlit run app.py
```

## Results and interpretation
The earlier README recorded approximately 77% accuracy and 0.62 attack recall for the separate-test experiment, and approximately 78% accuracy and 0.63 attack recall after class balancing and increasing the number of trees. These are historical figures from the previous preprocessing approach. They have not been reproduced with the corrected unknown-category handling, so do not treat them as the current model's verified performance. Run `python evaluate_model.py` and record its actual output before publishing updated metrics.

A recall near 0.63 means the model identified roughly 63% of the attack examples in that evaluation; it also missed a meaningful portion. Accuracy alone is not enough to judge an intrusion-detection model.

## Known limitations
- This project uses historical NSL-KDD records; it does not inspect live packets.
- The Streamlit demo asks for 11 values and fills the remaining model features with zero. Its predictions are illustrative and may not represent a complete connection record.
- The evaluation scripts now encode categories not seen during training as `-1` instead of silently replacing them with a different category.
- The categorical columns currently use `OrdinalEncoder`. One-hot encoding or a carefully designed preprocessing pipeline can be explored as a future improvement.
- The Isolation Forest script reports results on the same records used for fitting. This is not an independent test.
- The saved model and preprocessing files must be generated together and kept compatible.

## Future improvements
- Use a consistent preprocessing pipeline with explicit handling of unseen categories.
- Evaluate using the separate test set and save reproducible metrics.
- Improve the manual demo so it validates complete feature inputs.
- Explore live packet capture and feature extraction as a separate future development phase.
- Investigate recall-focused threshold tuning and multi-class attack classification.

## Responsible use
This is an educational prototype for learning and experimentation with a public benchmark dataset. It is not a production intrusion-detection system and should not be used as the sole basis for security decisions.
