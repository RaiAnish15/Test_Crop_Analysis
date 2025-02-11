'''App to showcase the Crop Price Analysis: Madhya Pradesh'''

# Importing the necessary libraries
import streamlit as st

import pandas as pd
import plotly.graph_objects as go
import numpy as np

import arch 
from arch import arch_model
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Title of the dashboard
st.title("Brinjal Price Analysis Across States")

# Uploading the Excel file
uploaded_file = st.file_uploader("Upload the State Modal Price Excel File", type=["xlsx"])

if uploaded_file is not None:
    # Reading the Excel file
    data = pd.read_excel(uploaded_file)
    
    # Assuming the first column is 'Price Date'
    data["Price Date"] = pd.to_datetime(data["Price Date"])
    states = list(data.columns[1:])  # Excluding 'Price Date' column

    # Sidebar for state selection
    selected_state = st.sidebar.selectbox('Select a State', states)

    # Plotting the price of Brinjal for the selected state
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data["Price Date"], 
        y=data[selected_state], 
        mode='lines', 
        name=f"Brinjal Price in {selected_state}",
        line=dict(color='purple', width=2)
    ))

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Modal Price (Rs./Quintal)",
        template="plotly_dark",
        font=dict(color="white"),
        hovermode="x unified",
        margin=dict(l=40, r=40, t=40, b=40),
        plot_bgcolor="black",
        paper_bgcolor="black",
        width=900,
        height=500,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Please upload the 'State_Modal_Price.xlsx' file to proceed.")
