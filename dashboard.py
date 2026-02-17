import streamlit as st
from engine import run

st.set_page_config(page_title="OSINT Threat Dashboard", layout="wide")

st.title("🛡 OSINT Financial Threat Intelligence Dashboard")

if st.button("Fetch Latest Threats"):
    data = run()

    for cluster in data:

        st.markdown("---")
        st.subheader(f"Priority Score: {cluster['priority_score']}")

        st.write("Indicators:", cluster["indicators"])
        st.write("Related Events:", cluster["count"])

        for event in cluster["events"]:

            st.markdown(f"""
            **Alert:** {event['text']}
            - Severity: {event['severity']}
            - Confidence: {event['confidence']}
            - Category: {event['category']}
            - Financial Threat: {event['financial_type']}
            """)
