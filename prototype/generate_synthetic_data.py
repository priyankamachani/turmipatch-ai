"""
TurmiPatch AI - Synthetic Wound Data Generator

This script creates synthetic wound-healing data for early AI testing.

The generated data is not real patient data.
It is only for research, prototyping, and concept development.

TurmiPatch AI is not a medical device, diagnostic tool, or treatment.
"""

import csv
import random
from pathlib import Path


OUTPUT_PATH = Path("prototype/sample-data/generated-wound-data.csv")

WOUND_TYPES = [
    "surgical",
    "burn",
    "abrasion",
    "pressure_ulcer",
    "diabetic",
]

MONITORING_DAYS = [1, 3, 7, 14, 21, 28]


def clamp(value, minimum, maximum):
    """
    Keep a number within a safe range.
    """
    return max(minimum, min(value, maximum))


def generate_patient_profile(patient_number):
    """
    Create a synthetic patient wound profile.
    """

    wound_type = random.choice(WOUND_TYPES)

    if wound_type == "abrasion":
        starting_size = random.randint(15, 35)
        healing_speed = random.uniform(0.72, 0.88)

    elif wound_type == "surgical":
        starting_size = random.randint(25, 50)
        healing_speed = random.uniform(0.65, 0.82)

    elif wound_type == "burn":
        starting_size = random.randint(25, 55)
        healing_speed = random.uniform(0.58, 0.78)

    elif wound_type == "pressure_ulcer":
        starting_size = random.randint(35, 70)
        healing_speed = random.uniform(0.45, 0.68)

    else:
        starting_size = random.randint(35, 75)
        healing_speed = random.uniform(0.40, 0.65)

    has_complication = random.random() < 0.25

    return {
        "patient_id": f"P{patient_number:03d}",
        "wound_type": wound_type,
        "starting_size": starting_size,
        "healing_speed": healing_speed,
        "has_complication": has_complication,
    }


def calculate_healing_progress(day_index, has_complication):
    """
    Create synthetic healing progress from 0 to 100.
    """

    base_progress = [8, 18, 38, 62, 78, 90][day_index]

    if has_complication:
        base_progress -= random.randint(10, 30)

    noise = random.randint(-5, 5)

    return clamp(base_progress + noise, 0, 100)


def generate_wound_record(profile, day, day_index):
    """
    Generate one wound monitoring record.
    """

    progress = calculate_healing_progress(day_index, profile["has_complication"])

    wound_size = profile["starting_size"] * (1 - (progress / 120))
    wound_size = round(clamp(wound_size, 1, profile["starting_size"] + 10), 1)

    severity_base = 10 - (progress / 10)

    redness = round(clamp(severity_base + random.uniform(-1.5, 1.5), 1, 10), 1)
    swelling = round(clamp(severity_base + random.uniform(-2, 1), 1, 10), 1)
    moisture = round(clamp(severity_base + random.uniform(-2, 2), 1, 10), 1)
    pain = round(clamp(severity_base + random.uniform(-2, 1.5), 1, 10), 1)

    temperature = round(36.5 + ((redness + swelling) / 20) + random.uniform(-0.2, 0.4), 1)

    if profile["has_complication"] and day >= 7:
        redness = clamp(redness + random.uniform(0.5, 1.5), 1, 10)
        swelling = clamp(swelling + random.uniform(0.5, 1.5), 1, 10)
        temperature = round(clamp(temperature + random.uniform(0.2, 0.8), 36.5, 39.0), 1)

    return {
        "patient_id": profile["patient_id"],
        "day": day,
        "wound_type": profile["wound_type"],
        "wound_size_mm": wound_size,
        "redness_score": round(redness, 1),
        "swelling_score": round(swelling, 1),
        "moisture_score": round(moisture, 1),
        "pain_score": round(pain, 1),
        "temperature_c": temperature,
        "healing_progress": progress,
        "complication_risk": "yes" if profile["has_complication"] else "no",
    }


def generate_dataset(number_of_patients=50):
    """
    Generate synthetic wound healing records.
    """

    records = []

    for patient_number in range(1, number_of_patients + 1):
        profile = generate_patient_profile(patient_number)

        for day_index, day in enumerate(MONITORING_DAYS):
            record = generate_wound_record(profile, day, day_index)
            records.append(record)

    return records


def save_dataset(records):
    """
    Save generated records as a CSV file.
    """

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "patient_id",
        "day",
        "wound_type",
        "wound_size_mm",
        "redness_score",
        "swelling_score",
        "moisture_score",
        "pain_score",
        "temperature_c",
        "healing_progress",
        "complication_risk",
    ]

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def main():
    """
    Main function to generate and save synthetic wound data.
    """

    random.seed(42)

    records = generate_dataset(number_of_patients=50)
    save_dataset(records)

    print("TurmiPatch AI synthetic dataset generated successfully.")
    print(f"Total records created: {len(records)}")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
