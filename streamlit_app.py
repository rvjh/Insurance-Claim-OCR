import streamlit as st
import requests

st.title("AI Insurance Claim System")

user_id = st.text_input("User ID")
text = st.text_area("Enter Claim Details")

image = st.file_uploader("Upload Accident Image")

if st.button("Submit Claim"):

    files = {
        "image": image.getvalue()
    }

    data = {
        "user_id": user_id,
        "text": text
    }

    res = requests.post("http://localhost:8000/claim", data=data, files=files)

    st.json(res.json())