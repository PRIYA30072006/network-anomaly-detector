import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import OrdinalEncoder

st.set_page_config(page_title="AI Network Anomaly Detector", page_icon="🛡️")

@st.cache_resource
def load_artifacts():
    model = joblib.load("model.pkl")
    encoder = joblib.load("encoders.pkl")
    columns = joblib.load("columns.pkl")

    if not isinstance(encoder, OrdinalEncoder):
        raise TypeError(
            "The saved encoder is not an OrdinalEncoder. "
            "Run `python save_model.py` to regenerate all model artifacts."
        )
    if list(encoder.feature_names_in_) != ["protocol_type", "service", "flag"]:
        raise ValueError("The saved encoder does not match the expected categorical columns.")
    if not hasattr(model, "classes_") or set(model.classes_) != {0, 1}:
        raise ValueError("The saved model must contain both classes: 0 (Normal) and 1 (Attack).")
    if len(columns) != 41 or len(set(columns)) != 41:
        raise ValueError("The saved feature-column list must contain 41 unique columns.")
    return model, encoder, columns


st.title("🛡️ AI Network Anomaly Detector")
st.write("Upload complete connection records as a CSV file for a dataset-trained demonstration.")
st.info(
    "This is a dataset-based prototype. It does not capture or monitor live network traffic. "
    "Each uploaded row must contain all 41 model features."
)

try:
    model, encoder, columns = load_artifacts()
except Exception as exc:
    st.error(f"Could not load compatible model artifacts: {exc}")
    st.stop()

uploaded_file = st.file_uploader(
    "Upload a CSV containing complete network connection records",
    type=["csv"]
)

if uploaded_file is not None:
    try:
        raw_data = pd.read_csv(uploaded_file)
    except Exception as exc:
        st.error(f"Could not read the CSV file: {exc}")
        st.stop()

    missing_columns = [column for column in columns if column not in raw_data.columns]
    if missing_columns:
        st.error(
            f"CSV is missing {len(missing_columns)} required feature columns: "
            + ", ".join(missing_columns)
        )
        st.stop()

    if raw_data.empty:
        st.error("The uploaded CSV contains no records.")
        st.stop()

    input_data = raw_data.loc[:, columns].copy()
    text_columns = ["protocol_type", "service", "flag"]
    numeric_columns = [column for column in columns if column not in text_columns]

    for column in numeric_columns:
        input_data[column] = pd.to_numeric(input_data[column], errors="coerce")

    if input_data[numeric_columns].isna().any().any():
        bad_columns = input_data[numeric_columns].columns[
            input_data[numeric_columns].isna().any()
        ].tolist()
        st.error("Missing or non-numeric values found in: " + ", ".join(bad_columns))
        st.stop()

    if input_data[text_columns].isna().any().any():
        st.error("Categorical fields protocol_type, service, and flag cannot be empty.")
        st.stop()

    try:
        input_data[text_columns] = encoder.transform(input_data[text_columns])
        predictions = model.predict(input_data)
        probabilities = model.predict_proba(input_data)
    except Exception as exc:
        st.error(f"Prediction failed. Check the CSV feature values and model artifacts: {exc}")
        st.stop()

    class_positions = {label: index for index, label in enumerate(model.classes_)}
    attack_scores = probabilities[:, class_positions[1]]

    results = pd.DataFrame({
        "Prediction": ["ATTACK" if value == 1 else "NORMAL" for value in predictions],
        "Attack model score (%)": (attack_scores * 100).round(1)
    })

    st.subheader("Prediction results")
    st.dataframe(results, use_container_width=True)
    st.caption(
        "Model scores are not calibrated probabilities or guarantees. "
        "Predictions depend on the quality and representativeness of the uploaded records."
    )
    st.write(f"Records analysed: {len(results):,}")
    st.write(f"Predicted attacks: {int((predictions == 1).sum()):,}")
    st.write(f"Predicted normal: {int((predictions == 0).sum()):,}")

st.caption(
    "Expected input: one row per connection, with all 41 NSL-KDD model feature columns. "
    "Do not include attack_type or difficulty_level as model input."
)
