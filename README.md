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
| `train_model.py` | Trains an Isolation Forest baseline on KDDTrain+ and evaluates it on the separate KDDTest+ file. |
| `train_supervised.py` | Trains and evaluates a Random Forest using a random split of KDDTrain+. |
| `test_on_realdata.py` | Trains on KDDTrain+ and evaluates on KDDTest+. |
| `test_improved.py` | Tests a class-balanced Random Forest with 300 trees and prints feature importance. |
| `evaluate_model.py` | Runs a reproducible held-out evaluation and prints a confusion matrix, classification report, and unseen-category counts. |
| `save_model.py` | Trains the model used by the Streamlit demo and saves the model, encoders, and feature-column list. |
| `app.py` | Runs the Streamlit demonstration using uploaded CSV records containing all 41 model features. |
| `model.pkl` | Saved Random Forest model used by the demo. |
| `encoders.pkl` | Saved encoders for the three categorical input columns. |
| `columns.pkl` | Feature-column order expected by the saved model. |
| `KDDTrain+.txt` | NSL-KDD training dataset. |
| `KDDTest+.txt` | NSL-KDD test dataset. |

## Requirements
The project was tested locally in a Python virtual environment. Use a supported Python version compatible with the installed scikit-learn and Streamlit releases. Install the dependencies from the repository root:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
python -m pip install -r requirements.txt
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

The `audit/corrections` branch includes model artifacts regenerated with the same `OrdinalEncoder` format expected by `app.py`. If you retrain or change preprocessing, regenerate all three artifact files together by running `python save_model.py` before launching the app.

To launch the manual-input demo:

```bash
streamlit run app.py
```

## Results and interpretation

Latest recorded run of `python evaluate_model.py` on the separate KDDTest+ file:

| Metric | Normal | Attack |
|---|---:|---:|
| Precision | 0.6644 | 0.9671 |
| Recall | 0.9718 | 0.6285 |
| F1-score | 0.7892 | 0.7619 |
| Support | 9,711 | 12,833 |

- **Accuracy:** 0.7764 (77.64%)
- **Confusion matrix** (rows = actual class; columns = predicted class; order = Normal, Attack):

```text
              Predicted Normal  Predicted Attack
Actual Normal             9437               274
Actual Attack             4767              8066
```

The model detected 8,066 of 12,833 attack records and missed 4,767. Its attack precision is high (96.71%), but attack recall is only 62.85%. This means many records predicted as attacks were attacks in this test, but the model still failed to identify a substantial share of actual attacks. Accuracy alone is not enough to judge an intrusion-detection model.

These figures are the output reported from the current `evaluate_model.py` run; rerun the script in your environment to reproduce them. Results can vary with library versions or environment changes.

## Issues identified during testing and ongoing corrective work

Testing and static review have identified several issues. Some implementation changes have now been made, but they must be run and verified in the project environment before they can be considered fully resolved.

| Finding | Change made / current status |
|---|---|
| The previous Streamlit form accepted only 11 of 41 features and filled the rest with zero. | Replaced the partial form with CSV upload requiring all 41 feature columns; added checks for missing columns, empty categorical values, and non-numeric feature values. Runtime verification is pending. |
| The Isolation Forest baseline was evaluated on its training records and used a contamination value derived from attack labels. | Revised it to fit on KDDTrain+ and evaluate on KDDTest+, with `contamination="auto"`. Runtime verification is pending. |
| Ordinal encoding assigns integer codes to nominal categories and may introduce artificial ordering. | Still present in the supervised Random Forest workflow and saved demo artifacts. Alternative one-hot preprocessing needs to be evaluated before changing the artifact format. |
| Dependency versions are not pinned. | Need to record the actual working environment versions before pinning dependencies; no versions have been guessed. |
| Dataset source citation is missing. | The canonical dataset source and citation details still need to be verified and added. |

The recorded KDDTest+ Random Forest evaluation reports 62.85% attack recall and 4,767 missed attack records. This is a significant detection weakness and remains an important target for further experiments. Do not treat the reported accuracy alone as evidence of a dependable intrusion-detection system.

**Verification status:** The changes above have been committed to this branch, but they have not yet been executed in the user's local environment after the latest edits. The earlier Random Forest metrics are prior reported output, not fresh test evidence for these new changes.

## Responsible use
This is an educational prototype for learning and experimentation with a public benchmark dataset. It is not a production intrusion-detection system and should not be used as the sole basis for security decisions.
