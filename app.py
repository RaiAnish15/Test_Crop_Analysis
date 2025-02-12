'''App to showcase the Crop Price Analysis: Madhya Pradesh'''

# Importing the necessary libraries
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from arch import arch_model
import os

# Title of the dashboard
st.title("Analysis Across States, Crops, and Districts of INDIA")

# Default image for the initial clean dashboard
default_image = "India Map.jpeg"  # Replace with your actual default image file

# Automatically reading the CSV files
price_file_path = "State_Modal_Price (1).csv"
volatility_file_path = "State_Conditional_Volatility.csv"
district_price_file_path = "District_Modal_price.csv"
district_volatility_file_path = "District_Conditional_Volatility.csv"
district_meteorological_file_path = "District_Meteorological.csv"

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

    # Reading the district-level meteorological data CSV file
    district_meteorological_data = pd.read_csv(district_meteorological_file_path)
    district_meteorological_data["Price Date"] = pd.to_datetime(district_meteorological_data["Price Date"])

    states = list(price_data.columns[1:])  # Excluding 'Price Date' column

    # Sidebar for state selection
    selected_state = st.sidebar.selectbox('Select a State', ['Select a State'] + states)

    if selected_state != 'Select a State':
        # Additional dropdown for state-level analysis type
        state_analysis_type = st.sidebar.selectbox('Select State Analysis Type', ['Select Analysis Type', 'Modal Price', 'Log Return', 'Conditional Volatility'])

        if state_analysis_type != 'Select Analysis Type':
            fig = go.Figure()

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

        # Extracting crops for the selected state
        crop_columns = [col for col in district_price_data.columns if col.startswith(selected_state + '_')]
        crops = list(set([col.replace(f"{selected_state}_", "").split('_')[0] for col in crop_columns]))

        # Sidebar for crop selection
        selected_crop = st.sidebar.selectbox('Select a Crop', ['Select a Crop'] + crops)

        # Extracting districts for the selected state and crop
        district_columns = [col for col in crop_columns if f"{selected_state}_{selected_crop}" in col]
        districts = [col.replace(f"{selected_state}_{selected_crop}_", "") for col in district_columns]

        # Sidebar for district selection if districts are available
        selected_district = None
        if districts:
            selected_district = st.sidebar.selectbox('Select a District', ['Select a District'] + districts)

        if selected_crop != 'Select a Crop':
            # Separate dropdowns for Analysis and GPR Plot
            analysis_selected = st.sidebar.selectbox('Select Analysis', ['Select Analysis', 'Modal Price', 'Log Return', 'Conditional Volatility', 'Temperature', 'Precipitation'])
            gpr_selected = st.sidebar.selectbox('Select GPR Plot', ['Select GPR Plot', '2D Plot', '3D Plot'])

            if analysis_selected != 'Select Analysis':
                fig = go.Figure()

                if selected_district != 'Select a District' and selected_district is not None:
                    full_district_column = f"{selected_state}_{selected_crop}_{selected_district}"

                    if analysis_selected == 'Modal Price':
                        district_y_values = district_price_data[full_district_column]
                        y_label = "Modal Price (Rs./Quintal)"
                        line_color = 'blue'
                    
                    elif analysis_selected == 'Log Return':
                        district_y_values = np.log(district_price_data[full_district_column]) - np.log(district_price_data[full_district_column].shift(1))
                        y_label = "Log Return"
                        line_color = 'red'

                    elif analysis_selected == 'Conditional Volatility':
                        district_y_values = district_volatility_data[full_district_column]
                        y_label = "Conditional Volatility"
                        line_color = 'cyan'

                    elif analysis_selected == 'Temperature':
                        temp_column = f"{selected_state}_{selected_district}_Temperature"
                        if temp_column in district_meteorological_data.columns:
                            district_y_values = district_meteorological_data[temp_column]
                            y_label = "Temperature (°C)"
                            line_color = 'orange'
                        else:
                            st.warning(f"Temperature data for {selected_district} not found.")
                            district_y_values = None

                    elif analysis_selected == 'Precipitation':
                        precip_column = f"{selected_state}_{selected_district}_Precipitation"
                        if precip_column in district_meteorological_data.columns:
                            district_y_values = district_meteorological_data[precip_column]
                            y_label = "Precipitation (mm)"
                            line_color = 'blue'
                        else:
                            st.warning(f"Precipitation data for {selected_district} not found.")
                            district_y_values = None

                    if district_y_values is not None:
                        fig.add_trace(go.Scatter(
                            x=price_data["Price Date"], 
                            y=district_y_values, 
                            mode='lines', 
                            name=f"{analysis_selected} in {selected_district} ({selected_crop}), {selected_state}",
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

            if gpr_selected != 'Select GPR Plot':
                gpr_file_path = f"GPR/{selected_state}_{gpr_selected.split()[0]}.gif"
                if os.path.exists(gpr_file_path):
                    st.video(gpr_file_path, format="video/gif", caption=f"{gpr_selected} for {selected_state}")
                else:
                    st.warning(f"{gpr_selected} for {selected_state} not found. Ensure the file name is '{selected_state}_{gpr_selected.split()[0]}.gif' and it's in the GPR folder.")

    else:
        st.image(default_image, caption="Brinjal Price Analysis", use_container_width=True)

except FileNotFoundError:
    st.error("The required CSV files were not found. Please make sure 'State_Modal_Price.csv', 'State_Conditional_Volatility.csv', 'District_Modal_Price.csv', 'District_Conditional_Volatility.csv', and 'District_Meteorological.csv' are in the working directory.")
