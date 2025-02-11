'''App to showcase the Crop Price Analysis: Madhya Pradesh'''

# Importing the necessary libraries
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from arch import arch_model

# Title of the dashboard
st.title("Brinjal Price Analysis Across States")

# Automatically reading the CSV files
price_file_path = "State_Modal_Price.csv"
volatility_file_path = "State_Conditional_Volatility.csv"

try:
    # Reading the price data CSV file
    price_data = pd.read_csv(price_file_path)
    price_data["Price Date"] = pd.to_datetime(price_data["Price Date"])
    
    # Reading the conditional volatility CSV file
    volatility_data = pd.read_csv(volatility_file_path)
    volatility_data["Price Date"] = pd.to_datetime(volatility_data["Price Date"])

    states = list(price_data.columns[1:])  # Excluding 'Price Date' column

    # Sidebar for state selection
    selected_state = st.sidebar.selectbox('Select a State', states)

    # Additional dropdown for analysis type
    analysis_type = st.sidebar.selectbox('Select Analysis Type', ['Modal Price', 'Log Return', 'Conditional Volatility'])

    # Plotting based on the selected analysis type
    fig = go.Figure()

    if analysis_type == 'Modal Price':
        y_values = price_data[selected_state]
        y_label = "Modal Price (Rs./Quintal)"
        line_color = 'purple'
    
    elif analysis_type == 'Log Return':
        y_values = np.log(price_data[selected_state]) - np.log(price_data[selected_state].shift(1))
        y_label = "Log Return"
        line_color = 'orange'

    elif analysis_type == 'Conditional Volatility':
        y_values = volatility_data[selected_state]
        y_label = "Conditional Volatility"
        line_color = 'green'

    fig.add_trace(go.Scatter(
        x=price_data["Price Date"], 
        y=y_values, 
        mode='lines', 
        name=f"{analysis_type} in {selected_state}",
        line=dict(color=line_color, width=2)
    ))

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title=y_label,
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

except FileNotFoundError:
    st.error("The required CSV files were not found. Please make sure 'State_Modal_Price.csv' and 'State_Conditional_Volatility.csv' are in the working directory.")
