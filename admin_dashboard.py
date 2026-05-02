import streamlit as st
import requests

st.title("📊 Insurance AI Admin Dashboard")

API_URL = "http://127.0.0.1:8000/admin/metrics"

if st.button("Load Metrics"):

    res = requests.get(API_URL)

    if res.status_code == 200:
        data = res.json()

        st.metric("Total Users", data["total_users"])
        st.metric("Total Claims", data["total_claims"])
        st.metric("Approved Claims", data["approved_claims"])
        st.metric("Rejected Claims", data["rejected_claims"])
        st.metric("Car Detected Cases", data["car_detected_cases"])

    else:
        st.error("Failed to load admin metrics")