# AI-Based Network Anomaly Detector

## Problem Statement
Traditional network security relies on rule-based systems (fixed signatures) to detect
attacks, which fail against new or evolving attack patterns. This project explores
whether machine learning can detect anomalous (attack) network traffic using the
NSL-KDD dataset — a benchmark dataset for intrusion detection research — by learning
patterns from historical connection records instead of hardcoded rules.

## Dataset
- **Source:** NSL-KDD (improved version of the KDD Cup 1999 dataset), a widely-used
  benchmark for intrusion detection research.
- **Training set:** KDDTrain+ (125,973 records)
- **Test set:** KDDTest+ (22,544 records) — a completely separate file, used to
  evaluate the model on traffic patterns it never saw during training.
- **Features:** 41 network connection attributes (e.g. duration, protocol type,
  bytes sent/received, connection flags, service type) plus an attack label.
- **Label conversion:** The original dataset has 23 specific attack types
  (e.g. neptune, smurf, satan). These were converted into a binary label —
  `0 = normal`, `1 = attack` — for this project's scope.

## Approach

### 1. Unsupervised Detection — Isolation Forest
Tried first, since real-world anomaly detection often has no labeled attack data.
Isolation Forest flags outliers based on statistical structure alone, without using
the attack labels during training.
- **Result: ~60% accuracy**
- **Why it struggled:** Attack and normal traffic in NSL-KDD statistically overlap
  in several features, so pure unsupervised outlier detection could not cleanly
  separate them.

### 2. Supervised Detection — Random Forest
Since labels were available, a Random Forest classifier was trained next.
- **Initial result (same-file train/test split): 100% accuracy**
- This was treated as a red flag rather than a success. NSL-KDD is known to contain
  near-duplicate records across splits, so a same-file split can let the model
  effectively memorize rather than generalize.
- **Corrected test (trained on KDDTrain+, evaluated on the separate KDDTest+ file):**
  - Accuracy: **77%**
  - Attack precision: **0.97** (very few false alarms when it flags an attack)
  - Attack recall: **0.62** (misses ~38% of actual attacks)

### 3. Tuning — Class Balancing + More Trees
Tried `class_weight="balanced"` and increased trees (100 → 300) to address the
class imbalance (67,343 normal vs 58,630 attack records) and improve recall.
- **Result: 78% accuracy, recall 0.63** — only a marginal improvement.
- This suggested the bottleneck was not model configuration but the underlying
  statistical overlap between certain attack types and normal traffic.

### 4. Feature Importance Analysis
Checked which features the Random Forest relied on most:
1. `src_bytes` (18.7%) — bytes sent
2. `dst_bytes` (10.4%) — bytes received
3. `flag` (8.5%) — connection status
4. `same_srv_rate` (8.2%)
5. `dst_host_same_srv_rate` (6.1%)

These align with security intuition: abnormal data volumes and repeated
connections to the same service are classic indicators of DoS and probing attacks.

## Key Limitation (Honest Trade-off)
The final model has **high precision (0.97) but moderate recall (0.62–0.63)** for
attacks. In practice, this means: when the model says "attack," it is almost always
right — but it misses a significant portion of real attacks (false negatives).

For a real intrusion detection system, this is a meaningful trade-off. Missing an
attack is generally more costly than investigating a false alarm, so a security team
would likely tune the threshold to prioritize recall over precision — accepting more
false alarms in exchange for catching more real attacks. This project did not pursue
that tuning further, in order to keep scope manageable, but it is the clear next step.

## Tech Stack
- Python 3.13
- pandas — data loading and preprocessing
- scikit-learn — Isolation Forest, Random Forest, preprocessing, evaluation

## How to Run
1. Install dependencies: `pip install pandas scikit-learn matplotlib`
2. Download the NSL-KDD dataset and place `KDDTrain+.txt` and `KDDTest+.txt`
   inside an `archive/` folder in the project directory.
3. Run:
   - `python explore_data.py` — inspect the dataset
   - `python train_model.py` — unsupervised Isolation Forest baseline
   - `python test_on_realdata.py` — supervised Random Forest, proper train/test split
   - `python test_improved.py` — tuned model + feature importance

## Possible Future Improvements
- Try gradient boosting algorithms (XGBoost, LightGBM) for potentially better recall
- Multi-class classification (predict specific attack type, not just normal/attack)
- Threshold tuning to explicitly prioritize recall for a security-first use case