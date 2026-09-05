import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

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
train_data["label"] = train_data["attack_type"].apply(lambda x: 0 if x == "normal" else 1)

# Encoders save pannanum, demo la user input convert panna venum adhukku
encoders = {}
text_columns = ["protocol_type", "service", "flag"]
for col in text_columns:
    le = LabelEncoder()
    train_data[col] = le.fit_transform(train_data[col])
    encoders[col] = le

X_train = train_data.drop(columns=["attack_type", "difficulty_level", "label"])
y_train = train_data["label"]

print("Training final model...")
clf = RandomForestClassifier(n_estimators=300, class_weight="balanced", random_state=42)
clf.fit(X_train, y_train)

# Model and encoders ah file ah save pannurom
joblib.dump(clf, "model.pkl")
joblib.dump(encoders, "encoders.pkl")
joblib.dump(list(X_train.columns), "columns.pkl")

print("Model saved successfully! (model.pkl, encoders.pkl, columns.pkl)")