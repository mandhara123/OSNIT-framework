import streamlit as st
from engine import run

st.title("OSINT Financial Threat Monitor")

if st.button("Scan News"):
    results = run()

    for r in results:
        st.subheader("Threat Detected")
        st.write("Category:", r["category"])
        st.write("Score:", r["score"])
        st.write(r["text"])
        st.divider()
