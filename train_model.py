"""Unsupervised Isolation Forest baseline evaluated on held-out KDDTest+ data.

The attack labels are used only for evaluation, not for preprocessing or fitting
the anomaly detector.
"""
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report

COLUMN_NAMES = [
    "duration", "protocol_type", "service", "flag", "src_bytes",
    "dst_bytes", "land", "wrong_fragment", "urgent", "hot",
    "num_failed_logins", "logged_in", "num_compromised", "root_shell",
    "su_attempted", "num_root", "num_file_creations", "num_shells",
    "num_access_files", "num_outbound_cmds", "is_host_login",
    "is_guest_login", "count", "srv_count", "serror_rate",
    "srv_serror_rate", "rerror_rate", "srv_rerror_rate", "same_srv_rate",
    "diff_srv_rate", "srv_diff_host_rate", "dst_host_count",
    "dst_host_srv_count", "dst_host_same_srv_rate", "dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate", "dst_host_srv_diff_host_rate",
    "dst_host_serror_rate", "dst_host_srv_serror_rate",
    "dst_host_rerror_rate", "dst_host_srv_rerror_rate",
    "attack_type", "difficulty_level"
]
CATEGORICAL_COLUMNS = ["protocol_type", "service", "flag"]


def load_dataset(path):
    data = pd.read_csv(path, names=COLUMN_NAMES)
    if data.shape[1] != len(COLUMN_NAMES):
        raise ValueError(
            f"{path} has {data.shape[1]} columns; expected {len(COLUMN_NAMES)}."
        )
    labels = (data["attack_type"] != "normal").astype(int)
    features = data.drop(columns=["attack_type", "difficulty_level"])
    return features, labels


def main():
    X_train, y_train = load_dataset("KDDTrain+.txt")
    X_test, y_test = load_dataset("KDDTest+.txt")

    # Encode nominal categories without imposing an integer order. Fit the
    # category columns on training data only, then align the test columns.
    X_train = pd.get_dummies(X_train, columns=CATEGORICAL_COLUMNS)
    X_test = pd.get_dummies(X_test, columns=CATEGORICAL_COLUMNS)
    X_test = X_test.reindex(columns=X_train.columns, fill_value=0)

    print("Training Isolation Forest on KDDTrain+...")
    model = IsolationForest(
        n_estimators=100,
        contamination="auto",
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train)

    # Isolation Forest returns 1 for inliers and -1 for outliers.
    predictions = (model.predict(X_test) == -1).astype(int)

    print("\nDataset sizes")
    print(f"Training records: {len(X_train):,}")
    print(f"Test records:     {len(X_test):,}")
    print("\nHeld-out KDDTest+ performance")
    print(classification_report(
        y_test,
        predictions,
        labels=[0, 1],
        target_names=["Normal", "Attack"],
        digits=4,
        zero_division=0
    ))


if __name__ == "__main__":
    main()
