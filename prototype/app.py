import streamlit as st
from PIL import Image
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="TurmiPatch AI",
    page_icon="🩹",
    layout="centered"
)

st.title("🩹 TurmiPatch AI")
st.subheader("AI-assisted wound recovery monitoring prototype")

st.warning(
    "Disclaimer: This is an early-stage research prototype only. "
    "It is not a certified medical device and must not be used for diagnosis, treatment, "
    "or clinical decision-making."
)

st.markdown("""
TurmiPatch AI explores how image-based monitoring, symptom tracking, and AI-inspired
risk scoring could support wound recovery observation in the future.
""")

st.divider()

st.header("1. Upload wound image")

uploaded_file = st.file_uploader(
    "Upload a wound image for prototype analysis",
    type=["jpg", "jpeg", "png"]
)

st.header("2. Enter visible symptoms")

pain = st.slider("Pain level", 0, 10, 3)
redness = st.slider("Redness level", 0, 10, 3)
swelling = st.slider("Swelling level", 0, 10, 2)
warmth = st.slider("Warmth around wound", 0, 10, 2)
healing_progress = st.slider("Visible healing progress", 0, 10, 5)

discharge = st.selectbox(
    "Visible discharge?",
    ["None", "Mild", "Moderate", "High"]
)

smell = st.selectbox(
    "Unusual smell?",
    ["No", "Mild", "Strong"]
)

st.header("3. Prototype analysis")


def calculate_risk_score(
    pain_level,
    redness_level,
    swelling_level,
    warmth_level,
    healing_level,
    discharge_level,
    smell_level
):
    score = 0

    score += pain_level * 1.2
    score += redness_level * 1.4
    score += swelling_level * 1.3
    score += warmth_level * 1.2

    if discharge_level == "Mild":
        score += 4
    elif discharge_level == "Moderate":
        score += 8
    elif discharge_level == "High":
        score += 12

    if smell_level == "Mild":
        score += 4
    elif smell_level == "Strong":
        score += 8

    # Better healing progress reduces risk
    score -= healing_level * 0.8

    return max(round(score, 2), 0)


def classify_risk(score):
    if score < 10:
        return "Low", "Continue normal observation and track healing progress."
    elif score < 22:
        return "Medium", "Monitor closely. Consider seeking medical advice if symptoms increase."
    else:
        return "High", "High risk signal in this prototype. Seek qualified medical advice."


if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded wound image", use_container_width=True)

    risk_score = calculate_risk_score(
        pain,
        redness,
        swelling,
        warmth,
        healing_progress,
        discharge,
        smell
    )

    risk_level, recommendation = classify_risk(risk_score)

    st.metric("Prototype Risk Score", risk_score)
    st.metric("Prototype Risk Level", risk_level)

    if risk_level == "Low":
        st.success(recommendation)
    elif risk_level == "Medium":
        st.warning(recommendation)
    else:
        st.error(recommendation)

    st.subheader("Input Summary")

    result_data = {
        "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Pain": [pain],
        "Redness": [redness],
        "Swelling": [swelling],
        "Warmth": [warmth],
        "Healing Progress": [healing_progress],
        "Discharge": [discharge],
        "Smell": [smell],
        "Risk Score": [risk_score],
        "Risk Level": [risk_level],
    }

    df = pd.DataFrame(result_data)
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download prototype result as CSV",
        data=csv,
        file_name="turmipatch_ai_result.csv",
        mime="text/csv"
    )

else:
    st.info("Upload an image to generate a prototype risk output.")

st.divider()

st.caption(
    "TurmiPatch AI v0.2.0 prototype | Research and innovation use only | "
    "Not medical advice"
)