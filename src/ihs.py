import pandas as pd
import numpy as np

prop_powertrain = pd.read_csv("data/powertrain_propulsion_system.csv")
prop_powertrain.rename(columns={"propulsion_system_design": "e_propulsion_system_design2"}, inplace=True)
prop_powertrain['e_propulsion_system_design2'] = prop_powertrain['e_propulsion_system_design2'].str.lower()
ihs = pd.read_csv("data/ihs.csv")

ihs_bis = ihs.loc[(ihs["region"] == "Western Europe") & (2020 < ihs['period_year']) & (ihs['period_year'] <= 2022) , :].reset_index(drop=True)

volumes = ihs_bis\
    .groupby(['region', 'period_year', 'e_propulsion_system_design', 'e_propulsion_system_design2', 'e_fuel_type'])\
    .agg({"sum_volume" : sum}).reset_index()
volumes['e_propulsion_system_design2'] = volumes['e_propulsion_system_design2'].str.lower()


def define_powertrain(row):

    if ((row['e_propulsion_system_design'] == 'ICE') | (row['e_propulsion_system_design'] == 'ICE: Stop/Start') ) & (row['e_fuel_type'] == 'DIESEL'):
        return "ICE-D"

    if (row['e_propulsion_system_design'] == 'ICE') | (row['e_propulsion_system_design'] == 'ICE: Stop/Start'):
        return "ICE"

    if (row['e_propulsion_system_design'] == 'CNG'):
        return "CNG"
    if (row['e_propulsion_system_design'] == "Hybrid-Mild") | (row['e_propulsion_system_design'] == "Hybrid-Full"):
        return "Hybrid"
    if (row['e_propulsion_system_design'] == "PHEV"):
        return "PHEV"
    if (row['e_propulsion_system_design'] == "Electric"):
        return "BEV"
    if (row['e_propulsion_system_design'] == "Fuel Cell"):
        return "FCEV"


volumes['powertrain'] = volumes.apply(lambda row: define_powertrain(row), axis=1)#pd.merge(volumes, prop_powertrain, on=['e_propulsion_system_design2'])

grouped=volumes.groupby(["powertrain", "period_year"])\
    .agg({"sum_volume": sum})\
    .transform({"sum_volume": lambda x: x / 1E6})