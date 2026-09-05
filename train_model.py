import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report

# Column names
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

# Load data
data = pd.read_csv("KDDTrain+.txt", names=column_names)

# STEP 1: binary label - 0 = normal, 1 = attack
data["label"] = data["attack_type"].apply(lambda x: 0 if x == "normal" else 1)

# STEP 2: text columns ah numbers ah convert pannurom
text_columns = ["protocol_type", "service", "flag"]
for col in text_columns:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])

# STEP 3: features (X) and labels (y) separate pannurom
X = data.drop(columns=["attack_type", "difficulty_level", "label"])
y = data["label"]

print("Total records:", len(X))
print("Normal:", (y == 0).sum(), "| Attack:", (y == 1).sum())

# STEP 4: scaling - ella numbers ah same range ku kondu varurom
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# STEP 5: Isolation Forest model
contamination_rate = (y == 1).sum() / len(y)
model = IsolationForest(n_estimators=100, contamination=contamination_rate, random_state=42)

print("\nTraining model... (idhu konjam neram edukkalam)")
model.fit(X_scaled)

# STEP 6: predictions
predictions = model.predict(X_scaled)
predictions = [1 if p == -1 else 0 for p in predictions]

# STEP 7: evaluate
print("\n--- Model Performance ---")
print(classification_report(y, predictions, target_names=["Normal", "Attack"]))