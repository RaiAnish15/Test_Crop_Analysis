'''App to showcase the Crop Price Analysis: Madhya Pradesh'''

# Importing the necessary libraries
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from arch import arch_model

# Title of the dashboard
st.title("Brinjal Price Analysis Across States and Districts")

# Default image for the initial clean dashboard
default_image = "India Map.jpeg"  # Replace with your actual default image file

# Automatically reading the CSV files
price_file_path = "State_Modal_Price.csv"
volatility_file_path = "State_Conditional_Volatility.csv"
district_price_file_path = "District_Modal_Price.csv"
district_volatility_file_path = "District_Conditional_Volatility.csv"

try:
    # Reading the price data CSV file
    price_data = pd.read_csv(price_file_path)
    price_data["Price Date"] = pd.to_datetime(price_data["Price Date"])
    
    # Reading the conditional volatility CSV file
    volatility_data = pd.read_csv(volatility_file_path)
    volatility_data["Price Date"] = pd.to_datetime(volatility_data["Price Date"])

    # Reading the district-level price data CSV file
    district_price_data = pd.read_csv(district_price_file_path)
    district_price_data["Price Date"] = pd.to_datetime(district_price_data["Price Date"])

    # Reading the district-level conditional volatility CSV file
    district_volatility_data = pd.read_csv(district_volatility_file_path)
    district_volatility_data["Price Date"] = pd.to_datetime(district_volatility_data["Price Date"])

    states = list(price_data.columns[1:])  # Excluding 'Price Date' column

    # Sidebar for state selection
    selected_state = st.sidebar.selectbox('Select a State', ['Select a State'] + states)

    if selected_state != 'Select a State':
        # Additional dropdown for state-level analysis type
        state_analysis_type = st.sidebar.selectbox('Select State Analysis Type', ['Modal Price', 'Log Return', 'Conditional Volatility'])

        # Extracting districts for the selected state
        district_columns = [col for col in district_price_data.columns if col.startswith(selected_state + '_')]
        districts = [col.replace(f"{selected_state}_", "") for col in district_columns]

        # Sidebar for district selection if districts are available
        selected_district = None
        if districts:
            selected_district = st.sidebar.selectbox('Select a District', ['Select a District'] + districts)

        # Plotting based on the selected analysis type
        fig = go.Figure()

        if selected_district == 'Select a District' or selected_district is None:
            if state_analysis_type == 'Modal Price':
                y_values = price_data[selected_state]
                y_label = "Modal Price (Rs./Quintal)"
                line_color = 'purple'
            
            elif state_analysis_type == 'Log Return':
                y_values = np.log(price_data[selected_state]) - np.log(price_data[selected_state].shift(1))
                y_label = "Log Return"
                line_color = 'orange'

            elif state_analysis_type == 'Conditional Volatility':
                y_values = volatility_data[selected_state]
                y_label = "Conditional Volatility"
                line_color = 'green'

            fig.add_trace(go.Scatter(
                x=price_data["Price Date"], 
                y=y_values, 
                mode='lines', 
                name=f"{state_analysis_type} in {selected_state}",
                line=dict(color=line_color, width=2)
            ))
        else:
            full_district_column = f"{selected_state}_{selected_district}"

            # Additional dropdown for district-level analysis type
            district_analysis_type = st.sidebar.selectbox('Select District Analysis Type', ['Modal Price', 'Log Return', 'Conditional Volatility'])

            if district_analysis_type == 'Modal Price':
                district_y_values = district_price_data[full_district_column]
                y_label = "Modal Price (Rs./Quintal)"
                line_color = 'blue'
            
            elif district_analysis_type == 'Log Return':
                district_y_values = np.log(district_price_data[full_district_column]) - np.log(district_price_data[full_district_column].shift(1))
                y_label = "Log Return"
                line_color = 'red'

            elif district_analysis_type == 'Conditional Volatility':
                district_y_values = district_volatility_data[full_district_column]
                y_label = "Conditional Volatility"
                line_color = 'cyan'

            fig.add_trace(go.Scatter(
                x=district_volatility_data["Price Date"], 
                y=district_y_values, 
                mode='lines', 
                name=f"{district_analysis_type} in {selected_district}, {selected_state}",
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
    else:
        st.image(default_image, caption="Brinjal Price Analysis", use_container_width=True)

except FileNotFoundError:
    st.error("The required CSV files were not found. Please make sure 'State_Modal_Price.csv', 'State_Conditional_Volatility.csv', 'District_Modal_Price.csv', and 'District_Conditional_Volatility.csv' are in the working directory.")
