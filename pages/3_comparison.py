

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Comparison")
st.write("Compare platforms or categories")

if 'df' not in st.session_state:
    st.warning("Please upload a file first in Data Upload page")
else:
    df = st.session_state['df']
    
    st.subheader("Select Columns")
    category_col = st.selectbox("Category", df.columns, key="cat")
    value_col = st.selectbox("Value", df.columns, key="val")
    
    # Multi-select for comparison
    options = st.multiselect(
        "Select items to compare",
        df[category_col].unique()
    )
    
    if options:
        filtered_df = df[df[category_col].isin(options)]
        comparison_data = filtered_df.groupby(category_col)[value_col].sum()
        
        st.bar_chart(comparison_data)
        
        st.subheader("Comparison Table")
        st.dataframe(comparison_data)


