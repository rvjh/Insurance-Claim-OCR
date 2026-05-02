import streamlit as st
import requests

st.title("🚗 Insurance Claim AI System")

API_URL = "http://127.0.0.1:8000/claim"

# INPUTS
user_id = st.text_input("User ID", "12345")
claim_text = st.text_area("Claim Text")

image = st.file_uploader("Upload Car Image", type=["png", "jpg", "jpeg"])

# SUBMIT BUTTON
if st.button("Submit Claim"):

    if image is None:
        st.error("Please upload an image")
        st.stop()

    files = {
        "image": (image.name, image.getvalue(), image.type)
    }

    data = {
        "user_id": user_id,
        "claim_text": claim_text
    }

    response = requests.post(API_URL, data=data, files=files)

    if response.status_code == 200:
        result = response.json()

        # SHOW SAME RESPONSE AS FASTAPI
        st.subheader("📌 Claim Result")

        st.write("### Status:", result["status"])
        st.write("### Message:", result["message"])
        st.write("### Car Detected:", result["car_detected"])
        st.write("### Confidence:", result["confidence"])

        st.write("### Timings:")
        st.json(result["timings"])

    else:
        st.error("API Error")
        st.write(response.text)