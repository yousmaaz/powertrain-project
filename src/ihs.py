import pandas as pd
import numpy as np



def define_powertrain(row):
    if ((row['e_propulsion_system_design'] == 'ICE') | (row['e_propulsion_system_design'] == 'ICE: Stop/Start')) &\
    ((row['e_fuel_type'] == 'DIESEL') | (row['e_fuel_type'] == 'DIESEL-CNG')):
        return "ICE-D"
    
    if ((row['e_propulsion_system_design'] == 'ICE') | (row['e_propulsion_system_design'] == 'ICE: Stop/Start')) &\
        ((row['e_fuel_type'] == 'GAS') | (row['e_fuel_type'] == 'GAS-CNG') |\
         (row['e_fuel_type'] == 'GAS-E100') | (row['e_fuel_type'] == 'GAS-E85') | \
         (row['e_fuel_type'] == 'GAS-LPG') | (row['e_fuel_type'] == 'GAS-M100')):
        return "ICE-G"

    if ((row['e_propulsion_system_design'] == 'ICE') | (row['e_propulsion_system_design'] == 'ICE: Stop/Start')) &\
        (row['e_fuel_type'] == 'CNG'):
        return "CNG"

    if ((row['e_propulsion_system_design'] == 'ICE') | (row['e_propulsion_system_design'] == 'ICE: Stop/Start')) &\
        (row['e_fuel_type'] == 'Hydrogen'):
        return "HICEV"

    if ((row['e_propulsion_system_design'] == 'ICE') | (row['e_propulsion_system_design'] == 'ICE: Stop/Start')) &\
        (row['e_fuel_type'] == 'LPG'):
        return "ICE-LPG"

    if  ((row['e_propulsion_system_design'] == "Hybrid-Mild") |\
        ( (row['e_propulsion_system_design'] == "Hybrid-Full") &\
         (row['e_propulsion_system_design2'] in ('HEV-Full (DIESEL)', 'HEV-Full (GAS)', 'HEV-Full (GAS-E100)',
                                                  'HEV-Full (GAS-E85)', 'HEV-Full (GAS-M100)', 'HEV-Full (LPG)')))):
        return "HEV"

    if (row['e_propulsion_system_design'] == "Hybrid-Full") &\
        ((row['e_propulsion_system_design2'] in ("PHEV-Full (DIESEL)" , "PHEV-Full (GAS)" , "PHEV-Full (GAS-E100)"))):
        return "PHEV"
    if (row['e_propulsion_system_design'] == "Electric"):
        return "BEV"

    if (row['e_propulsion_system_design'] == "Electric") &\
         ((row['e_fuel_type'] in ('GAS', 'GAS-E100'))):
        return "REEV"

    if (row['e_propulsion_system_design'] == "Fuel Cell"):
        return "FCEV"


      

#ihs = pd.read_csv("/home/cdsw/data/ihs-202302.csv")

def get_volumes_ihs(ihs):
  
  volumes = ihs\
      .groupby(['region', 'period_year', 'e_propulsion_system_design', 'e_propulsion_system_design2', 'e_fuel_type'])\
      .agg({"sum_volume" : sum}).reset_index()

  volumes['powertrain'] = volumes.apply(lambda row: define_powertrain(row), axis=1)


  agg_volume_powertrain = volumes.groupby(["region","period_year","powertrain"])\
      .agg({"sum_volume": sum})\
      .transform({"sum_volume": lambda x: x / 1E6})

  sum_agg = agg_volume_powertrain.reset_index().groupby(['region','period_year']).sum().rename(columns={"sum_volume": "sum_powertrain"})

  agg_volume_powertrain_per = pd.merge(agg_volume_powertrain.reset_index(), sum_agg, on=["region","period_year"])\
  .assign(ratio_volume= lambda x: x["sum_volume"] / x["sum_powertrain"])\
  .rename(columns={"period_year": "year", "powertrain": "powertrain_type"})\
  .assign(region = lambda x: x['region'].str.lower())
  
  return agg_volume_powertrain_per

#agg_volume_powertrain_per.to_csv("data/output/ihs_volume_output.csv", index=False)