import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import train_test_split
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

data = pd.read_csv("KDDTrain+.txt", names=column_names)
data["label"] = (data["attack_type"] != "normal").astype(int)

text_columns = ["protocol_type", "service", "flag"]
X = data.drop(columns=["attack_type", "difficulty_level", "label"])
y = data["label"]

# Split before fitting the encoder so preprocessing learns categories from training rows only.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
X_train[text_columns] = encoder.fit_transform(X_train[text_columns])
X_test[text_columns] = encoder.transform(X_test[text_columns])

print("Training Random Forest (supervised)...")
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)
predictions = clf.predict(X_test)

print("\n--- Supervised Model Performance ---")
print(classification_report(y_test, predictions, target_names=["Normal", "Attack"]))
