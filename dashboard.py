import streamlit as st
from engine import run
from streamlit_autorefresh import st_autorefresh

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(page_title="OSINT Threat Dashboard", layout="wide")

# ---------------- AUTO REFRESH ---------------- #
st_autorefresh(interval=60000, key="datarefresh")

# ---------------- TITLE ---------------- #
st.title("🛡 OSINT Financial Threat Intelligence Dashboard")

# ---------------- FETCH DATA ---------------- #
data = run()

if not data:
    st.warning("No threats detected.")
    st.stop()

# ---------------- DASHBOARD ---------------- #
for cluster in data:

    st.markdown("---")
    st.subheader(f"🔥 Priority Score: {cluster['priority_score']}")

    st.write("Indicators:", cluster["indicators"])
    st.write("Related Events:", cluster["count"])
    st.write("Trend:", cluster.get("trend", "UNKNOWN"))

    # ---------- EVENTS ---------- #
    for event in cluster["events"]:

        with st.container():

            # Title
            st.markdown(f"### 🚨 {event.get('title','No Title')}")

            # Summary
            st.write(event.get("summary", "No summary available"))

            # Metadata Row
            col1, col2, col3 = st.columns(3)

            col1.metric("Severity", event["severity"])
            col2.metric("Confidence", event["confidence"])
            col3.metric("Score", event["score"])

            # Extra Info
            st.caption(f"Source: {event.get('source','Unknown')}")

            if event.get("category"):
                st.write("Category:", ", ".join(event["category"]))

            if event.get("financial_type"):
                st.write("Financial Threat:", event["financial_type"])

            # Link
            if event.get("url"):
                st.link_button("Read Full Report", event["url"])

            st.markdown("---")
