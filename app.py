import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
from fpdf import FPDF

# Dark theme
st.set_page_config(page_title="Journalists Trust Analyzer", layout="wide")
st.markdown("""
<style>
.stApp {background-color: #0E1117; color: white;}
</style>
""", unsafe_allow_html=True)

st.title("📊 Journalists Trust Analyzer")

tab1, tab2 = st.tabs(["📁 Upload Excel File", "🤖 AI Text Analyzer"])

# ========== TAB 1: UPLOAD FILE ==========
with tab1:
    st.subheader("Upload your Excel or CSV file")
    uploaded_file = st.file_uploader("Choose a file", type=["xlsx", "xls", "csv"], key="file_uploader")

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
        st.success("File uploaded successfully!")
        st.dataframe(df)

        platforms = ["Facebook", "Twitter/X", "Instagram", "TikTok", "YouTube", "Snapchat", "AI"]
        df_filtered = df[df["Platform"].isin(platforms)]

        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Trust % by Platform")
            fig_bar = px.bar(df_filtered, x="Platform", y="Trust (%)", 
                             color="Platform", 
                             color_discrete_map={
                                 "Facebook":"#1877F2", "Twitter/X":"#1DA1F2", "Instagram":"#E1306C",
                                 "TikTok":"#FF0000", "YouTube":"#4CAF50", "Snapchat":"#00AFF0", "AI":"#FFA500"
                             })
            fig_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig_bar, use_container_width=True)

        with col2:
            st.subheader("Trust vs Daily Usage")
            fig_scatter = px.scatter(df_filtered, x="Daily Usage (%)", y="Trust (%)", 
                                     size="Trust (%)", color="Platform", hover_name="Platform", size_max=60,
                                     color_discrete_map={
                                         "Facebook":"#1877F2", "Twitter/X":"#1DA1F2", "Instagram":"#E1306C",
                                         "TikTok":"#FF0000", "YouTube":"#4CAF50", "Snapchat":"#00AFF0", "AI":"#FFA500"
                                     })
            fig_scatter.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig_scatter, use_container_width=True)

        st.divider()
        # PDF + Excel Download same as before
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_filtered.to_excel(writer, index=False)
        excel_data = output.getvalue()

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=14)
        pdf.cell(200, 10, txt="Journalists Trust Report", ln=True, align='C')
        pdf_output = pdf.output(dest='S').encode('latin1')

        col1, col2 = st.columns(2)
        with col1: st.download_button("📊 Download Excel", data=excel_data, file_name="Report.xlsx")
        with col2: st.download_button("📄 Download PDF", data=pdf_output, file_name="Report.pdf")

# ========== TAB 2: AI TEXT ANALYZER ==========
with tab2:
    st.subheader("Write about political and economic situations")
    text_input = st.text_area("📝 Write your analysis here:", height=200)

    if st.button("🔍 Analyze with AI"):
        if text_input:
            data = []
            platforms = ["Facebook", "Twitter/X", "Instagram", "TikTok", "YouTube", "Snapchat", "AI"]
            text_lower = text_input.lower()
            base_trust, base_usage = 50, 50

            if "crisis" in text_lower: base_trust -= 20
            if "lost trust" in text_lower: base_usage += 20
            if "alternative" in text_lower: base_usage += 25

            for platform in platforms:
                trust = base_trust + (10 if platform.lower() in text_lower else 0)
                usage = base_usage + (15 if platform.lower() in text_lower else 0)
                data.append({"Platform": platform, "Trust (%)": max(0,min(100,trust)), "Daily Usage (%)": max(0,min(100,usage))})
            
            df_ai = pd.DataFrame(data)
            st.dataframe(df_ai)

            col1, col2 = st.columns(2)
            with col1:
                fig_bar2 = px.bar(df_ai, x="Platform", y="Trust (%)", color="Platform")
                fig_bar2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color="white")
                st.plotly_chart(fig_bar2, use_container_width=True)
            with col2:
                fig_scatter2 = px.scatter(df_ai, x="Daily Usage (%)", y="Trust (%)", size="Trust (%)", color="Platform", hover_name="Platform")
                fig_scatter2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color="white")
                st.plotly_chart(fig_scatter2, use_container_width=True)
        else:
            st.warning("Please write some text")





