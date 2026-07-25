import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Journalists' Trust in Social Media Platforms", layout="wide")
st.title("Mapping Journalists' Trust in Social Media Platforms")
st.write("A general analytical dashboard for media research and data visualization.")

# Sample general data (you can replace it with real study results)
data = {
    "Platform": ["Facebook", "Twitter/X", "Instagram", "TikTok", "YouTube", "Snapchat", "AI"],
    "Trust (%)": [25, 68, 40, 15, 55, 45, 60],
    "Daily Usage (%)": [85, 72, 60, 45, 70, 55, 50]
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

import io
from fpdf import FPDF

st.divider()
st.subheader("Download Report")

# 1. Prepare Excel file
output = io.BytesIO()
with pd.ExcelWriter(output, engine='openpyxl') as writer:
    df.to_excel(writer, index=False, sheet_name='Trust Data')
excel_data = output.getvalue()

# 2. Prepare PDF file
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=14)
pdf.cell(200, 10, txt="Journalists Trust Report", ln=True, align='C')
pdf.ln(10)
pdf.set_font("Arial", size=11)

for i, row in df.iterrows():
    line = f"{row['Platform']}: Trust = {row['Trust (%)']}% | Daily Usage = {row['Daily Usage (%)']}%"
    pdf.cell(200, 10, txt=line, ln=True)

pdf_output = pdf.output(dest='S').encode('latin1')

# 3. Show 2 buttons side by side
col1, col2 = st.columns(2)
with col1:
    st.download_button(
        label="📊 Download Excel",
        data=excel_data,
        file_name="Journalists_Trust_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
with col2:
    st.download_button(
        label="📄 Download PDF",
        data=pdf_output,
        file_name="Journalists_Trust_Report.pdf",
        mime="application/pdf"
    )

st.caption("Tip: Right-click on any chart > 'Save image as' to download the chart as PNG")
