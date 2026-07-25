
import streamlit as st
import pandas as pd

st.title("Comparison")

if 'df' not in st.session_state:
    st.warning("Please upload a file first in Data Upload page")
else:
    df = st.session_state['df']

    category_col = st.selectbox("Choose Category Column", df.columns)
    value_col = st.selectbox("Choose Value Column", df.columns)

    options = st.multiselect("Pick items to compare", df[category_col].unique())

    if options:
        filtered_df = df[df[category_col].isin(options)]
        comparison_data = filtered_df.groupby(category_col)[value_col].sum()

        st.bar_chart(comparison_data)
        st.write("Numbers:")
        st.dataframe(comparison_data)
