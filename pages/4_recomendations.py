
import streamlit as st
import pandas as pd

st.title("AI Recommendations")
st.write("Smart insights from your data")

if 'df' not in st.session_state:
    st.warning("Please upload a file first in Data Upload page")
else:
    df = st.session_state['df']

    st.subheader("Top Insights")

    # Auto find numeric and categorical columns
    num_cols = df.select_dtypes(include='number').columns
    cat_cols = df.select_dtypes(include='object').columns

    if len(num_cols) > 0 and len(cat_cols) > 0:
        top_cat = cat_cols[0]
        top_num = num_cols[0]

        # Find best performing
        best = df.groupby(top_cat)[top_num].sum().idxmax()
        best_value = df.groupby(top_cat)[top_num].sum().max()

        st.success(f"1. Best performing {top_cat}: {best} with total {best_value}")

        # Find worst
        worst = df.groupby(top_cat)[top_num].sum().idxmin()
        st.warning(f"2. Lowest performing {top_cat}: {worst}")

        st.info(f"3. Total records: {len(df)}")
        st.info(f"4. Average {top_num}: {df[top_num].mean():.2f}")
    else:
        st.write("Upload data with numbers and categories to see recommendations")
