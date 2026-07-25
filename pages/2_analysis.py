
import streamlit as st
import pandas as pd

st.title("Data Upload")
st.write("Upload your Excel or CSV file here")

uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xlsx'])

if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.session_state['df'] = df # <-- This line saves the data

    st.success("File uploaded successfully!")
    st.dataframe(df.head())
    st.write(f"Total rows: {len(df)}")


