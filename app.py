import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Journalists' Trust in Social Media Platforms", layout="wide")
st.title("Alternative Media'Mapping Journalists' Trust in Social Media Platforms")
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

import streamlit as st
import pandas as pd
import plotly.express as px
import io
from fpdf import FPDF

st.set_page_config(page_title="Journalists Trust Analyzer", layout="wide")
st.title("📊 Journalists Trust & Social Media Analyzer")

# 1. File Upload
uploaded_file = st.file_uploader("Upload your Excel file here", type=["xlsx", "xls"])

if uploaded_file is not None:
    # Read the file
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    
    st.success("File uploaded successfully!")
    st.dataframe(df)

    # 2. Plot the chart
    st.subheader("Trust vs Daily Usage")
    fig = px.scatter(df, 
                     x="Trust (%)", 
                     y="Daily Usage (%)", 
                     size="Trust (%)", 
                     color="Platform",
                     hover_name="Platform",
                     size_max=60)
    st.plotly_chart(fig, use_container_width=True)

    # 3. Download Buttons
    st.divider()
    st.subheader("Download Report")

    # Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
    excel_data = output.getvalue()

    # PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Journalists Trust Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=11)
    for i, row in df.iterrows():
        line = f"{row['Platform']}: Trust = {row['Trust (%)']}% | Usage = {row['Daily Usage (%)']}%"
        pdf.cell(200, 10, txt=line, ln=True)
    pdf_output = pdf.output(dest='S').encode('latin1')

    col1, col2 = st.columns(2)
    with col1:
        st.download_button("📊 Download Excel", data=excel_data, file_name="Report.xlsx")
    with col2:
        st.download_button("📄 Download PDF", data=pdf_output, file_name="Report.pdf")

else:
    st.info("👆 Please upload an Excel file to start the analysis")

st.caption("Note: Excel file must have columns: Platform, Trust (%), Daily Usage (%)")

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
import re
import random
from fpdf import FPDF

# Dark theme
st.set_page_config(page_title="Journalists Trust Analyzer", layout="wide")
st.markdown("""
<style>
.stApp {background-color: #0E1117; color: white;}
</style>
""", unsafe_allow_html=True)

st.title("📊 Journalists Trust Analyzer")
st.write("Note: Excel file must have columns: Platform, Trust (%), Daily Usage (%)")

tab1, tab2 = st.tabs(["📁 Upload Excel File", "🤖 AI Text Analyzer"])

# ========== FUNCTION FOR AI ==========
def analyze_text_with_ai(text):
    platforms = ["Facebook", "Twitter/X", "Instagram", "TikTok", "YouTube", "Snapchat", "AI"]
    results = []
    text_lower = text.lower()

    for platform in platforms:
        trust, usage = None, None
        
        # 1. Try to find numbers in text like "Facebook trust 80 usage 90"
        trust_match = re.search(rf"{platform}.*?trust.*?(\d{{1,3}})", text, re.IGNORECASE)
        usage_match = re.search(rf"{platform}.*?usage.*?(\d{{1,3}})|{platform}.*?daily.*?
