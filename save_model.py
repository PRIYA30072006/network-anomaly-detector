import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OrdinalEncoder
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
train_data["label"] = (train_data["attack_type"] != "normal").astype(int)

text_columns = ["protocol_type", "service", "flag"]
encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
train_data[text_columns] = encoder.fit_transform(train_data[text_columns])

X_train = train_data.drop(columns=["attack_type", "difficulty_level", "label"])
y_train = train_data["label"]

print("Training final Random Forest model...")
clf = RandomForestClassifier(n_estimators=300, class_weight="balanced", random_state=42)
clf.fit(X_train, y_train)

# Save the model and its matching preprocessing metadata together.
joblib.dump(clf, "model.pkl")
joblib.dump(encoder, "encoders.pkl")
joblib.dump(list(X_train.columns), "columns.pkl")

print("Saved model.pkl, encoders.pkl (OrdinalEncoder), and columns.pkl.")
