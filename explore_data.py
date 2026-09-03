import pandas as pd

# NSL-KDD dataset la column names kudukapadala, so namba manually define pannanum
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

# Data ah load pannuvom
data = pd.read_csv("archive/KDDTrain+.txt", names=column_names)

# First 5 rows paakalam
print(data.head())

# Evlo rows, evlo columns irukku nu paakalam
print("\nShape of data (rows, columns):", data.shape)

# Attack types enna ellam irukku nu paakalam
print("\nAttack types found:\n", data["attack_type"].value_counts())