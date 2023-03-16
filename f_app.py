import pandas as pd
import streamlit as st

# Cache the dataframe so it's only loaded once
@st.cache_data
def load_data():
    return pd.DataFrame(
        {
            "id ": 1,
            "bill_no." : 1,
            "name" : "Minal",
            "company" : "Aspire",
            "Mobile Number" : 1234567890,
            "E-mail" : "aar@gmail.com",
            "Date" : 12/9/2012,
            "Type_of_bill" : "",
            "Quantity" : 1,
            "Description" : "",
            "Amount" : 4234567.00
        }
    ).rename_index()

# Boolean to resize the dataframe, stored as a session state variable
st.checkbox("Use container width", value=False, key="use_container_width")

df = load_data()

# Display the dataframe and allow the user to stretch the dataframe
# across the full width of the container, based on the checkbox value
st.dataframe(df, use_container_width=st.session_state.use_container_width)