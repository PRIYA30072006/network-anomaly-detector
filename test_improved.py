import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OrdinalEncoder
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

train_data = pd.read_csv("KDDTrain+.txt", names=column_names)
test_data = pd.read_csv("KDDTest+.txt", names=column_names)

for data in (train_data, test_data):
    data["label"] = (data["attack_type"] != "normal").astype(int)

text_columns = ["protocol_type", "service", "flag"]
encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
train_data[text_columns] = encoder.fit_transform(train_data[text_columns])
test_data[text_columns] = encoder.transform(test_data[text_columns])

X_train = train_data.drop(columns=["attack_type", "difficulty_level", "label"])
y_train = train_data["label"]
X_test = test_data.drop(columns=["attack_type", "difficulty_level", "label"])
y_test = test_data["label"]

print("Training improved Random Forest (balanced + 300 trees)...")
clf = RandomForestClassifier(n_estimators=300, class_weight="balanced", random_state=42)
clf.fit(X_train, y_train)
predictions = clf.predict(X_test)

print("\n--- Improved Model Performance ---")
print(classification_report(y_test, predictions, target_names=["Normal", "Attack"]))

print("\n--- Top 10 Feature Importances ---")
importances = pd.Series(clf.feature_importances_, index=X_train.columns)
print(importances.sort_values(ascending=False).head(10))
