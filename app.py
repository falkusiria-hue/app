import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Mapping Journalists' Trust in Social Media")

platform = st.selectbox(
    "Select Platform:",
    ["Facebook", "Twitter/X", "Instagram", "TikTok", "YouTube"]
)

st.write(f"You selected: {platform}")

data = {
    'Platform': ['Facebook', 'Twitter/X', 'Instagram', 'TikTok', 'YouTube'],
    'Trust': [65, 45, 70, 55, 80]
}
df = pd.DataFrame(data)

fig = px.bar(df, x='Platform', y='Trust', title='Trust Level by Platform')
st.plotly_chart(fig)
