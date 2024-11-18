import streamlit as st
import pandas as pd

# Load and clean the data
data = pd.read_csv("장애인현황.csv")

# Rename the first column for clarity
data.rename(columns={data.columns[0]: "Type"}, inplace=True)

# Initialize session state
if "ID" not in st.session_state:
    st.session_state["ID"] = "None"

ID = st.session_state["ID"]

with st.sidebar:
    st.caption(f'{ID}님 접속중')

with st.form("input"):
    # User selects disability types or "전체"
    types = st.multiselect("장애 유형", data['Type'].unique(), default=["전체"])
    submitted = st.form_submit_button("조회")

    if submitted:
        name_list = []
        # Filter selected data
        result = pd.DataFrame({'Year': data.columns[1:]})  # Create DataFrame with years

        for t in types:
            selected_data = data[data['Type'] == t].iloc[:, 1:].T  # Transpose to get years as rows
            selected_data.columns = [t]  # Rename column to the type
            selected_data.reset_index(inplace=True)
            selected_data.rename(columns={"index": "Year"}, inplace=True)
            result = pd.merge(result, selected_data, on="Year", how="left")  # Merge data
            name_list.append(t)

        # Ensure 'Year' is sorted and numeric for proper plotting
        result['Year'] = result['Year'].astype(int)

        # Display line chart
        st.line_chart(data=result, x='Year', y=name_list, use_container_width=True)
