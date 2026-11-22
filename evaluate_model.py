"""Reproducible evaluation of the Random Forest on the separate NSL-KDD test set."""
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import OrdinalEncoder

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
        raise ValueError(f"{path} has {data.shape[1]} columns; expected {len(COLUMN_NAMES)}.")
    data["label"] = (data["attack_type"] != "normal").astype(int)
    return data


def main():
    train_data = load_dataset("KDDTrain+.txt")
    test_data = load_dataset("KDDTest+.txt")

    encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
    train_data[CATEGORICAL_COLUMNS] = encoder.fit_transform(train_data[CATEGORICAL_COLUMNS])

    # Count categories in KDDTest+ that were not present in KDDTrain+.
    unseen_counts = {}
    for column, known_categories in zip(CATEGORICAL_COLUMNS, encoder.categories_):
        unseen_counts[column] = int((~test_data[column].isin(known_categories)).sum())

    test_data[CATEGORICAL_COLUMNS] = encoder.transform(test_data[CATEGORICAL_COLUMNS])

    feature_columns = [
        column for column in COLUMN_NAMES
        if column not in ("attack_type", "difficulty_level")
    ]
    X_train = train_data[feature_columns]
    y_train = train_data["label"]
    X_test = test_data[feature_columns]
    y_test = test_data["label"]

    model = RandomForestClassifier(
        n_estimators=300,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )
    print("Training Random Forest on KDDTrain+...")
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    print("\nDataset sizes")
    print(f"Training records: {len(X_train):,}")
    print(f"Test records:     {len(X_test):,}")
    print("\nUnseen test categories (record counts)")
    for column, count in unseen_counts.items():
        print(f"{column}: {count:,}")

    print("\nConfusion matrix (rows=true, columns=predicted; order: Normal, Attack)")
    print(confusion_matrix(y_test, predictions, labels=[0, 1]))

    print("\nClassification report")
    print(classification_report(
        y_test, predictions, labels=[0, 1],
        target_names=["Normal", "Attack"], digits=4, zero_division=0
    ))


if __name__ == "__main__":
    main()
