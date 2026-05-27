"""
TurmiPatch AI - Early Healing Score Prototype

This script uses synthetic wound-healing data to calculate a basic healing
risk score. It is an early research prototype and is not intended for medical use.

Disclaimer:
TurmiPatch AI is not a medical device, diagnostic tool, or treatment.
This code is for concept development and AI experimentation only.
"""

import csv
from pathlib import Path


DATA_PATH = Path("prototype/sample-data/wound-healing-sample.csv")


def calculate_risk_score(row):
    """
    Calculate a simple wound risk score.

    Higher score = higher risk.
    This is rule-based logic, not a trained medical AI model.
    """

    wound_size = float(row["wound_size_mm"])
    redness = float(row["redness_score"])
    swelling = float(row["swelling_score"])
    moisture = float(row["moisture_score"])
    pain = float(row["pain_score"])
    temperature = float(row["temperature_c"])

    score = 0

    # Wound size contribution
    if wound_size > 50:
        score += 25
    elif wound_size > 30:
        score += 15
    elif wound_size > 15:
        score += 8

    # Redness contribution
    if redness >= 8:
        score += 20
    elif redness >= 5:
        score += 10

    # Swelling contribution
    if swelling >= 8:
        score += 20
    elif swelling >= 5:
        score += 10

    # Moisture imbalance contribution
    if moisture >= 8:
        score += 15
    elif moisture >= 5:
        score += 8

    # Pain contribution
    if pain >= 8:
        score += 15
    elif pain >= 5:
        score += 8

    # Temperature contribution
    if temperature >= 38.0:
        score += 20
    elif temperature >= 37.5:
        score += 10

    return min(score, 100)


def classify_risk(score):
    """
    Convert risk score into simple risk category.
    """

    if score >= 70:
        return "High"
    elif score >= 40:
        return "Medium"
    return "Low"


def generate_recommendation(risk_level):
    """
    Generate a basic non-medical recommendation.
    """

    if risk_level == "High":
        return "Potential delayed healing risk detected. Clinical review may be needed."
    elif risk_level == "Medium":
        return "Monitor wound progress closely and continue tracking symptoms."
    return "Healing indicators appear stable in this sample record."


def analyse_wound_data():
    """
    Read synthetic data and print AI-style healing risk outputs.
    """

    if not DATA_PATH.exists():
        print(f"Data file not found: {DATA_PATH}")
        return

    with DATA_PATH.open("r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        print("TurmiPatch AI - Healing Score Test")
        print("----------------------------------")

        for row in reader:
            risk_score = calculate_risk_score(row)
            risk_level = classify_risk(risk_score)
            recommendation = generate_recommendation(risk_level)

            print(
                f"Patient: {row['patient_id']} | "
                f"Day: {row['day']} | "
                f"Risk Score: {risk_score}/100 | "
                f"Risk Level: {risk_level} | "
                f"Recommendation: {recommendation}"
            )


if __name__ == "__main__":
    analyse_wound_data()
