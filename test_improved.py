import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

column_names = [
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

train_data = pd.read_csv("archive/KDDTrain+.txt", names=column_names)
test_data = pd.read_csv("archive/KDDTest+.txt", names=column_names)

train_data["label"] = train_data["attack_type"].apply(lambda x: 0 if x == "normal" else 1)
test_data["label"] = test_data["attack_type"].apply(lambda x: 0 if x == "normal" else 1)

text_columns = ["protocol_type", "service", "flag"]
for col in text_columns:
    le = LabelEncoder()
    le.fit(train_data[col])
    train_data[col] = le.transform(train_data[col])
    test_data[col] = test_data[col].apply(lambda x: x if x in le.classes_ else le.classes_[0])
    test_data[col] = le.transform(test_data[col])

X_train = train_data.drop(columns=["attack_type", "difficulty_level", "label"])
y_train = train_data["label"]
X_test = test_data.drop(columns=["attack_type", "difficulty_level", "label"])
y_test = test_data["label"]

print("Training improved Random Forest (balanced + more trees)...")

# IMPROVEMENT 1: class_weight="balanced" - imbalance handle pannum
# IMPROVEMENT 2: n_estimators=300 - more trees, better learning
clf = RandomForestClassifier(
    n_estimators=300,
    class_weight="balanced",
    random_state=42
)
clf.fit(X_train, y_train)

predictions = clf.predict(X_test)

print("\n--- Improved Model Performance ---")
print(classification_report(y_test, predictions, target_names=["Normal", "Attack"]))

# IMPROVEMENT 3: Feature importance - endha columns real ah help pannudhu nu paakalam
print("\n--- Top 10 Most Important Features ---")
importances = pd.Series(clf.feature_importances_, index=X_train.columns)
print(importances.sort_values(ascending=False).head(10))