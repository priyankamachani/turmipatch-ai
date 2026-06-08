import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
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

This version includes **basic image colour analysis** to estimate visual redness,
brightness, and red-pixel ratio from the uploaded image.
""")

st.divider()

st.header("1. Upload wound image")

uploaded_file = st.file_uploader(
    "Upload a wound image for prototype analysis",
    type=["jpg", "jpeg", "png"]
)

st.header("2. Enter visible symptoms")

pain = st.slider("Pain level", 0, 10, 3)
redness = st.slider("Visible redness level", 0, 10, 3)
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


def calculate_symptom_risk_score(
    pain_level,
    redness_level,
    swelling_level,
    warmth_level,
    healing_level,
    discharge_level,
    smell_level
):
    """Rule-based risk score using user-reported symptoms."""
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


def analyse_image_colour(image):
    """
    Basic image colour analysis.

    This is not a medical model. It only extracts simple image-level features:
    - image width and height
    - average red, green, blue values
    - average brightness
    - red pixel ratio
    - redness index
    """

    image_rgb = image.convert("RGB")
    image_array = np.array(image_rgb)

    height, width, _ = image_array.shape

    red_channel = image_array[:, :, 0].astype(float)
    green_channel = image_array[:, :, 1].astype(float)
    blue_channel = image_array[:, :, 2].astype(float)

    avg_red = float(np.mean(red_channel))
    avg_green = float(np.mean(green_channel))
    avg_blue = float(np.mean(blue_channel))

    brightness = float(np.mean((red_channel + green_channel + blue_channel) / 3))

    # Red-pixel heuristic:
    # A pixel is treated as red-dominant when red is meaningfully higher than green and blue.
    red_dominant_pixels = (
        (red_channel > green_channel * 1.15) &
        (red_channel > blue_channel * 1.15) &
        (red_channel > 90)
    )

    red_pixel_ratio = float(np.mean(red_dominant_pixels) * 100)

    # Redness index: how much red dominates over green/blue on average.
    redness_index = avg_red - ((avg_green + avg_blue) / 2)
    redness_index = max(round(redness_index, 2), 0)

    return {
        "Image Width": width,
        "Image Height": height,
        "Average Red": round(avg_red, 2),
        "Average Green": round(avg_green, 2),
        "Average Blue": round(avg_blue, 2),
        "Average Brightness": round(brightness, 2),
        "Red Pixel Ratio (%)": round(red_pixel_ratio, 2),
        "Redness Index": redness_index,
    }


def calculate_image_risk_score(image_features):
    """
    Converts basic image features into a simple prototype image risk score.

    This is a heuristic for demonstration only.
    It is not trained on clinical data.
    """

    red_ratio = image_features["Red Pixel Ratio (%)"]
    redness_index = image_features["Redness Index"]
    brightness = image_features["Average Brightness"]

    image_score = 0

    # Higher red ratio increases image-informed risk.
    if red_ratio > 35:
        image_score += 10
    elif red_ratio > 20:
        image_score += 7
    elif red_ratio > 10:
        image_score += 4
    else:
        image_score += 1

    # Higher redness index increases image-informed risk.
    if redness_index > 55:
        image_score += 8
    elif redness_index > 35:
        image_score += 5
    elif redness_index > 20:
        image_score += 3

    # Very dark images may reduce confidence, so add a small caution score.
    if brightness < 70:
        image_score += 3

    return round(image_score, 2)


def classify_risk(score):
    if score < 14:
        return "Low", "Continue normal observation and track healing progress."
    elif score < 30:
        return "Medium", "Monitor closely. Consider seeking medical advice if symptoms increase."
    else:
        return "High", "High risk signal in this prototype. Seek qualified medical advice."


if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded wound image", use_container_width=True)

    symptom_risk_score = calculate_symptom_risk_score(
        pain,
        redness,
        swelling,
        warmth,
        healing_progress,
        discharge,
        smell
    )

    image_features = analyse_image_colour(image)
    image_risk_score = calculate_image_risk_score(image_features)

    # Combined prototype score:
    # Symptom score has higher weight because image analysis is only basic heuristic.
    combined_risk_score = round((symptom_risk_score * 0.7) + (image_risk_score * 0.3), 2)

    risk_level, recommendation = classify_risk(combined_risk_score)

    st.subheader("Prototype Risk Output")

    col1, col2, col3 = st.columns(3)
    col1.metric("Symptom Risk Score", symptom_risk_score)
    col2.metric("Image Risk Score", image_risk_score)
    col3.metric("Combined Risk Score", combined_risk_score)

    st.metric("Prototype Risk Level", risk_level)

    if risk_level == "Low":
        st.success(recommendation)
    elif risk_level == "Medium":
        st.warning(recommendation)
    else:
        st.error(recommendation)

    st.divider()

    st.subheader("Basic Image Colour Analysis")

    st.markdown(
        "These values are simple image-level features. "
        "They are included to demonstrate early computer-vision style analysis."
    )

    image_feature_df = pd.DataFrame([image_features])
    st.dataframe(image_feature_df, use_container_width=True)

    st.divider()

    st.subheader("Input and Result Summary")

    result_data = {
        "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Pain": [pain],
        "Visible Redness": [redness],
        "Swelling": [swelling],
        "Warmth": [warmth],
        "Healing Progress": [healing_progress],
        "Discharge": [discharge],
        "Smell": [smell],
        "Image Width": [image_features["Image Width"]],
        "Image Height": [image_features["Image Height"]],
        "Average Brightness": [image_features["Average Brightness"]],
        "Red Pixel Ratio (%)": [image_features["Red Pixel Ratio (%)"]],
        "Redness Index": [image_features["Redness Index"]],
        "Symptom Risk Score": [symptom_risk_score],
        "Image Risk Score": [image_risk_score],
        "Combined Risk Score": [combined_risk_score],
        "Risk Level": [risk_level],
    }

    result_df = pd.DataFrame(result_data)
    st.dataframe(result_df, use_container_width=True)

    csv = result_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download prototype result as CSV",
        data=csv,
        file_name="turmipatch_ai_colour_analysis_result.csv",
        mime="text/csv"
    )

else:
    st.info("Upload an image to generate a prototype risk output.")

st.divider()

st.caption(
    "TurmiPatch AI v0.3.0 prototype | Basic image colour analysis | "
    "Research and innovation use only | Not medical advice"
)
