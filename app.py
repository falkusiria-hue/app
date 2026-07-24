import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Journalists' Trust in Social Media Platforms", layout="wide")
st.title("Mapping Journalists' Trust in Social Media Platforms")
st.write("A general analytical dashboard for media research and data visualization.")

# Sample general data (you can replace it with real study results)
data = {
    "Platform": ["Facebook", "Twitter/X", "Instagram", "TikTok", "YouTube"],
    "Trust (%)": [25, 68, 40, 15, 55],
    "Daily Usage (%)": [85, 72, 60, 45, 70]
}
df = pd.DataFrame(data)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Journalists' Trust in Each Platform")
    fig1 = px.bar(df, x="Platform", y="Trust (%)", color="Platform")
    st.plotly_chart(fig1)

with col2:
    st.subheader("Daily Usage vs Trust")
    fig2 = px.scatter(df, x="Daily Usage (%)", y="Trust (%)",
                      size="Trust (%)", color="Platform", text="Platform")
    st.plotly_chart(fig2)

st.info("Insight: Journalists may use certain platforms heavily while trusting others more — a gap that can inspire new media solutions.")
