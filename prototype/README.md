# TurmiPatch AI Prototype

This folder contains the first working Streamlit prototype for TurmiPatch AI.

## Features

- Wound image upload
- Symptom tracking sliders
- Rule-based prototype risk scoring
- Risk level classification
- Result summary table
- CSV export
- Medical safety disclaimer

## How to Run Locally

From the root of the repository:

```bash
cd prototype
pip install -r requirements.txt
streamlit run app.py
```

## Important Disclaimer

This is an early-stage research prototype only.
It is not a certified medical device and must not be used for diagnosis,
treatment, or clinical decision-making.

## Suggested GitHub Release

After adding this prototype, publish a new release:

`v0.2.0 – Interactive Prototype`

## Future Improvements

- Add real computer vision model
- Add wound area segmentation
- Add healing progress comparison between images
- Add patient history tracking
- Add clinician-facing dashboard
- Add public dataset experimentation