#streamlit
import streamlit as st
import pandas as pd

import pandas as pd
import numpy as np
from functools import reduce
from fuel_cost import calculate_fuel_cost, calculate_elec_price


def generate_form():

    powertrain_type = st.sidebar.selectbox("Powertrain Type", ["FCEV", "BEV", "ICEV", "PHEV"])
    region = st.sidebar.selectbox("Region", ["western europe", "eastern europe", "north america", "asia"])

    # if st.sidebar.checkbox("Indicator Fuel Type"):
    #     fuel_type = st.sidebar.selectbox("Fuel Type", ["Gasoline", "Diesel", "CNG", "LPG"])
    #     fuel_price = st.sidebar.number_input("Fuel Price (in $)", value=0.0, step=0.1)
    #     fuel_consumption = st.sidebar.number_input("Fuel Consumption (in L/100km)", value=0.0, step=0.1)
    #     indicator_euro_seven_impact_fuel = st.sidebar.checkbox("Indicator Euro Seven Impact Fuel")
    #
    # else:
    #     fuel_type = None
    #     fuel_price = None
    #     fuel_consumption = None
    #     indicator_euro_seven_impact_fuel = False
    #
    #
    #
    # if st.sidebar.checkbox("Indicator Electricity"):
    #     elec_cons = st.sidebar.number_input("Electricity Consumption (in kWh/100km)", value=0.0, step=0.1)
    #     elec_price = st.sidebar.number_input("Electricity Price (in $/kWh)", value=0.0, step=0.01)
    # else:
    #     elec_cons = None
    #     elec_price = None
    #
    # if st.sidebar.checkbox("Indicator hydrogen"):
    #     hydrogen_price = st.sidebar.number_input("Hydrogen Price (in $/kg)", value=0.0, step=0.1)
    #     hydrogen_consumption = st.sidebar.number_input("Hydrogen Consumption (in kg/100km)", value=0.0, step=0.1)
    # else:
    #     hydrogen_price = None
    #     hydrogen_consumption  = None
    #
    # indicator_abdule = st.sidebar.checkbox("Indicator Abdule")
    # if indicator_abdule:
    #     adblue_consumption = st.sidebar.number_input("AdBlue Consumption (in L/100km)", value=0.0, step=0.1)
    #     adblue_price = st.sidebar.number_input("AdBlue Price (in $/L)", value=0.0, step=0.1)
    # else:
    #     adblue_consumption = None
    #     adblue_price = None

    return  ({
        "powertrain_type": powertrain_type,
        "region": region,
        # "fuel_type": fuel_type,
        # "fuel_price": fuel_price,
        # "fuel_consumption": fuel_consumption,
        # "indicator_euro_seven_impact_fuel": indicator_euro_seven_impact_fuel,
        # "elec_cons": elec_cons,
        # "elec_price": elec_price,
        # "hydrogen_price": hydrogen_price,
        # "hydrogen_consumption": hydrogen_consumption,
        # "indicator_abdule": indicator_abdule,
        # "adblue_consumption": adblue_consumption,
        # "adblue_price": adblue_price

    })





@st.cache(allow_output_mutation=True)
def get_data():
    euro_seven = pd.read_csv("data/euro_seven_impact.csv")
    eng_price_evol = pd.read_csv("data/energy_price_evolution.csv")
    return euro_seven, eng_price_evol


col1, col2 = st.columns(2)

with col1:
    with st.form('Form1'):
        st.selectbox('Select flavor', ['Vanilla', 'Chocolate'], key=1)
        st.slider(label='Select intensity', min_value=0, max_value=100, key=4)
        submitted1 = st.form_submit_button('Submit 1')

with col2:
    with st.form('Form2'):
        st.selectbox('Select Topping', ['Almonds', 'Sprinkles'], key=2)
        st.slider(label='Select Intensity', min_value=0, max_value=100, key=3)
        submitted2 = st.form_submit_button('Submit 2')

# euro_seven, eng_price_evol = get_data()
#
# # Create the sidebar
# st.sidebar.title("Powertrain Forms")
#
# forms = []
#
# # Create an "Add Form" button
# if st.sidebar.button("Add Form"):
#     forms.append(generate_form())
#
# # Create a "Remove Form" button
# if st.sidebar.button("Remove Form"):
#     forms.pop()
#
#
#
# lDf = []
#
# if st.sidebar.button("Calculate Fuel Price"):
#     for i, form in enumerate(forms):
#         df_ = calculate_fuel_cost(forms[i], euro_seven, eng_price_evol)
#         df_['powertrain_type'] = forms[i]['powertrain_type']
#         df_['region'] = forms[i]['region']
#         lDf.append(df_)
#
#     st.write("Fuel Price Data")
#     dfs = pd.concat(lDf)
#     st.dataframe(dfs)
#
#     # fuel_price = calculate_fuel_cost(input_fuel_cost, euro_seven, eng_price_evol)
#     # s = calculate_elec_price(input_fuel_cost, eng_price_evol, year_calcul=2021)
#     st.write("Fuel Price Data")
#     # st.dataframe(fuel_price)
#     # st.dataframe(fuel_price)
#

