import streamlit as st
import pandas as pd
import joblib

# Model and encoders load pannurom
model = joblib.load("model.pkl")
encoders = joblib.load("encoders.pkl")
columns = joblib.load("columns.pkl")

st.title("🛡️ AI Network Anomaly Detector")
st.write("Enter connection details below to check if it's Normal or an Attack.")

st.markdown("---")

# User input fields
col1, col2 = st.columns(2)

with col1:
    duration = st.number_input("Duration (seconds)", min_value=0, value=0)
    protocol_type = st.selectbox("Protocol Type", encoders["protocol_type"].classes_)
    service = st.selectbox("Service", encoders["service"].classes_)
    flag = st.selectbox("Flag", encoders["flag"].classes_)
    src_bytes = st.number_input("Source Bytes (data sent)", min_value=0, value=0)
    dst_bytes = st.number_input("Destination Bytes (data received)", min_value=0, value=0)

with col2:
    logged_in = st.selectbox("Logged In?", [0, 1])
    count = st.number_input("Connection Count (same host)", min_value=0, value=1)
    srv_count = st.number_input("Service Count", min_value=0, value=1)
    same_srv_rate = st.slider("Same Service Rate", 0.0, 1.0, 0.5)
    diff_srv_rate = st.slider("Different Service Rate", 0.0, 1.0, 0.0)

st.markdown("---")

if st.button("🔍 Check Connection"):
    # Default values for rest of the 41 columns (real deployment la ellame irukum,
    # demo ku namba key features mattum kudukurom, baaki default 0 vachukurom)
    input_data = {col: 0 for col in columns}

    input_data["duration"] = duration
    input_data["protocol_type"] = encoders["protocol_type"].transform([protocol_type])[0]
    input_data["service"] = encoders["service"].transform([service])[0]
    input_data["flag"] = encoders["flag"].transform([flag])[0]
    input_data["src_bytes"] = src_bytes
    input_data["dst_bytes"] = dst_bytes
    input_data["logged_in"] = logged_in
    input_data["count"] = count
    input_data["srv_count"] = srv_count
    input_data["same_srv_rate"] = same_srv_rate
    input_data["diff_srv_rate"] = diff_srv_rate

    # Correct column order la DataFrame create pannurom
    input_df = pd.DataFrame([input_data])[columns]

    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0]

    if prediction == 1:
        st.error(f"🚨 ATTACK DETECTED (confidence: {probability[1]*100:.1f}%)")
    else:
        st.success(f"✅ NORMAL TRAFFIC (confidence: {probability[0]*100:.1f}%)")

st.markdown("---")
st.caption("Note: This demo uses the NSL-KDD dataset for training. Predictions are simulated on manually entered values, not live network traffic.")