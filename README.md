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

Testing has identified the following areas that need attention. The project is currently in a testing-and-correction phase, and work is focused on investigating and addressing these findings before treating the implementation as complete.

| Finding from testing/review | Why it matters | Current status |
|---|---|---|
| The Streamlit demo accepts 11 of the model's 41 input features and fills the remaining 30 with zero. | The submitted values do not represent a complete network connection record, so the displayed prediction is illustrative only. | Under investigation; the input and feature-handling design needs correction. |
| The Isolation Forest baseline is evaluated on the same records used for fitting. | This does not measure performance on unseen data. Its contamination value is also calculated from known attack labels, so the experiment is not fully label-independent. | Evaluation methodology needs correction and clearer separation from the supervised experiments. |
| The categorical features use `OrdinalEncoder`. | Integer codes can imply an artificial order between nominal categories, which may affect tree splits. | Alternative categorical preprocessing is being assessed and must be compared using the held-out test set. |
| The dependency file does not pin package versions. | Different installations may use different library versions; serialized model files can also be sensitive to scikit-learn version changes. | The working environment versions need to be recorded before dependency versions are pinned. |
| The dataset description does not yet include a direct source/reference citation. | Readers should be able to identify and verify the benchmark dataset used. | Dataset source details need to be added and checked. |

The separate KDDTrain+/KDDTest+ evaluation is the current evidence for the reported Random Forest metrics. The recorded result shows 62.85% attack recall and 4,767 missed attack records. Improving attack detection without creating an unacceptable increase in false alarms is an important part of the ongoing testing work.

These findings are not being presented as completed fixes. They are the issues identified so far, and the implementation and evaluation will be updated only after the corresponding changes have been tested.

## Responsible use
This is an educational prototype for learning and experimentation with a public benchmark dataset. It is not a production intrusion-detection system and should not be used as the sole basis for security decisions.
