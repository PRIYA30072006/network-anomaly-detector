import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import OrdinalEncoder

model = joblib.load("model.pkl")
encoder = joblib.load("encoders.pkl")
columns = joblib.load("columns.pkl")

# Existing model artifacts may still use the old LabelEncoder format.
if not isinstance(encoder, OrdinalEncoder):
    st.error("The saved model files are outdated. Run `python save_model.py` to regenerate model.pkl, encoders.pkl, and columns.pkl, then restart this app.")
    st.stop()
text_columns = ["protocol_type", "service", "flag"]

st.title("🛡️ AI Network Anomaly Detector")
st.write("Enter selected connection details for a dataset-trained demonstration.")
st.info("This is a manual-input prototype. It does not capture or monitor live network traffic.")

col1, col2 = st.columns(2)
with col1:
    duration = st.number_input("Duration (seconds)", min_value=0, value=0)
    protocol_type = st.selectbox("Protocol Type", encoder.categories_[0])
    service = st.selectbox("Service", encoder.categories_[1])
    flag = st.selectbox("Flag", encoder.categories_[2])
    src_bytes = st.number_input("Source Bytes (data sent)", min_value=0, value=0)
    dst_bytes = st.number_input("Destination Bytes (data received)", min_value=0, value=0)

with col2:
    logged_in = st.selectbox("Logged In?", [0, 1])
    count = st.number_input("Connection Count (same host)", min_value=0, value=1)
    srv_count = st.number_input("Service Count", min_value=0, value=1)
    same_srv_rate = st.slider("Same Service Rate", 0.0, 1.0, 0.5)
    diff_srv_rate = st.slider("Different Service Rate", 0.0, 1.0, 0.0)

if st.button("🔍 Check Connection"):
    input_data = {col: 0 for col in columns}
    input_data.update({
        "duration": duration,
        "protocol_type": protocol_type,
        "service": service,
        "flag": flag,
        "src_bytes": src_bytes,
        "dst_bytes": dst_bytes,
        "logged_in": logged_in,
        "count": count,
        "srv_count": srv_count,
        "same_srv_rate": same_srv_rate,
        "diff_srv_rate": diff_srv_rate,
    })

    input_df = pd.DataFrame([input_data])[columns]
    input_df[text_columns] = encoder.transform(input_df[text_columns])

    prediction = model.predict(input_df)[0]
    scores = model.predict_proba(input_df)[0]

    if prediction == 1:
        st.error(f"🚨 Model prediction: ATTACK (model score: {scores[1] * 100:.1f}%)")
    else:
        st.success(f"✅ Model prediction: NORMAL (model score: {scores[0] * 100:.1f}%)")

    st.caption("The model score is not a calibrated probability or a guarantee.")

st.caption("Only 11 of the 41 model features are entered here; the other features are set to zero. Treat this as an illustrative demo, not a reliable network assessment.")
