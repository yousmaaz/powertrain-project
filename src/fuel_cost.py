import pandas as pd
import numpy as np
from functools import reduce
import numpy_financial as npf


#euro_seven = pd.read_csv("data/euro_seven_impact.csv")
#eng_price_evol = pd.read_csv("data/energy_price_evolution.csv")
#input_fuel_df = pd.read_csv("data/input_fuel.csv")

def get_euro_seven_impact_fuel(input_fuel_cost, euro_seven_input):
    # TODO Check if fuel_type exists before filtering


    request = (euro_seven_input['region'] == input_fuel_cost['region']) & (euro_seven_input['fuel_type'] == input_fuel_cost['fuel_type'])

    euro_seven_value = euro_seven_input.loc[request, ["year","extra_fuel_consumption"]].reset_index(drop=True)


    return euro_seven_value

def calculate_fuel_price(input_fuel_cost, eng_price_evol, year_calcul=2021):

    fuel_evol = eng_price_evol.loc[(eng_price_evol['region'] == input_fuel_cost['region']) & (
            eng_price_evol['energie_type'] == input_fuel_cost['fuel_type']), :].reset_index(drop=True)
    
#    print(fuel_evol)

    start_index = fuel_evol.index[fuel_evol['year'] == year_calcul].tolist()[0]

    for i in range(start_index, len(fuel_evol)):
        if fuel_evol.loc[i, 'year'] == year_calcul:
            fuel_evol.loc[i, "fuel_price"] = input_fuel_cost['fuel_price']

        elif (fuel_evol.loc[i, 'year'] >= year_calcul):
            fuel_evol.loc[i, "fuel_price"] = fuel_evol.loc[i - 1, "fuel_price"] * (
                    1 + (fuel_evol.loc[i - 1 , "value"] / 100))
        else:
            fuel_evol.loc[i, "fuel_price"] = 0


    return fuel_evol[['year', 'fuel_price']]

def calculate_elec_price(input_fuel_cost, eng_price_evol, year_calcul=2021):

    elec_evol = eng_price_evol.loc[(eng_price_evol['region'] == input_fuel_cost['region']) & (
            eng_price_evol['energie_type'] == "Electricity"), :].reset_index(drop=True)



    start_index = elec_evol.index[elec_evol['year'] == year_calcul].tolist()[0]

    for i in range(start_index, len(elec_evol)):
        if elec_evol.loc[i, 'year'] == year_calcul:
            elec_evol.loc[i, "elec_price"] = input_fuel_cost['elec_price']

        elif (elec_evol.loc[i, 'year'] >= year_calcul):
            elec_evol.loc[i, "elec_price"] = elec_evol.loc[i - 1, "elec_price"] * (
                    1 + (elec_evol.loc[i -1, "value"] / 100))
        else:
            elec_evol.loc[i, "elec_price"] = 0


    return elec_evol[['year', 'elec_price']]


def calculate_hydrogen_price(input_fuel_cost, eng_price_evol, year_calcul=2021):

    h_evol = eng_price_evol.loc[(eng_price_evol['region'] == input_fuel_cost['region']) & (
            eng_price_evol['energie_type'] == "Hydrogen"), :].reset_index(drop=True)

    start_index = h_evol.index[h_evol['year'] == year_calcul].tolist()[0]

    for i in range(start_index, len(h_evol)):
        if h_evol.loc[i, 'year'] == year_calcul:
            h_evol.loc[i, "hydrogen_price"] = input_fuel_cost['hydrogen_price']

        elif (h_evol.loc[i, 'year'] >= year_calcul):
            h_evol.loc[i, "hydrogen_price"] = h_evol.loc[i - 1, "hydrogen_price"] * (
                    1 + (h_evol.loc[i-1, "value"] / 100))
        else:
            h_evol.loc[i, "hydrogen_price"] = 0


    return h_evol[['year', 'hydrogen_price']]

def calculate_adblue_price(input_fuel_cost, eng_price_evol, year_calcul=2021):

    h_evol = eng_price_evol.loc[(eng_price_evol['region'] == input_fuel_cost['region']) & (
            eng_price_evol['energie_type'] == "Adblue"), :].reset_index(drop=True)

    start_index = h_evol.index[h_evol['year'] == year_calcul].tolist()[0]

    for i in range(start_index, len(h_evol)):
        if h_evol.loc[i, 'year'] == year_calcul:
            h_evol.loc[i, "adblue_price"] = input_fuel_cost['adblue_price']

        elif (h_evol.loc[i, 'year'] >= year_calcul):
            h_evol.loc[i, "adblue_price"] = h_evol.loc[i - 1, "adblue_price"] * (
                    1 + (h_evol.loc[i-1, "value"] / 100))
        else:
            h_evol.loc[i, "adblue_price"] = 0


    return h_evol[['year', 'adblue_price']]


def calculate_fuel_cost(input_fuel_cost, euro_seven,eng_price_evol, year_process=2021, end_year_process=2040):
    years_ = range(year_process, end_year_process + 1)

    if (input_fuel_cost["fuel_type"] not in ['', 'nan',  np.nan, None]):
        
        fuel_price = calculate_fuel_price(input_fuel_cost, eng_price_evol, year_calcul=year_process)
    else:
        
        fuel_price = pd.DataFrame({"year": years_ , "fuel_price" : np.repeat(0, end_year_process + 1 - year_process)})

    if input_fuel_cost["indicator_euro_seven_impact_fuel"]:
        impact_seven = get_euro_seven_impact_fuel(input_fuel_cost, euro_seven)
    else:
        impact_seven = pd.DataFrame({"year": years_ , "extra_fuel_consumption" : np.repeat(0, end_year_process + 1 - year_process)})

    if  (input_fuel_cost["elec_price"] not in ['', 'nan',  np.nan, None]):
        elec_price = calculate_elec_price(input_fuel_cost, eng_price_evol, year_calcul=year_process)
    else:
        elec_price = pd.DataFrame({"year": years_ , "elec_price" : np.repeat(0, end_year_process + 1 - year_process)})

    if  (input_fuel_cost["hydrogen_price"] not in ['', 'nan',  np.nan, None]):
        hydrogen_price = calculate_hydrogen_price(input_fuel_cost, eng_price_evol, year_calcul=year_process)
    else:
        hydrogen_price = pd.DataFrame({"year": years_ , "hydrogen_price" : np.repeat(0, end_year_process + 1 - year_process)})

    if  (input_fuel_cost["adblue_price"] not in ['', 'nan',  np.nan, None]) :
        adblue_price = calculate_adblue_price(input_fuel_cost, eng_price_evol, year_calcul=year_process)
    else:
        adblue_price = pd.DataFrame({"year": years_ , "adblue_price" : np.repeat(0, end_year_process + 1 - year_process)})

    if  (input_fuel_cost["fuel_consumption"] not in ['', 'nan',  np.nan, None]):
        fuel_consumption = pd.DataFrame({"year": years_, "fuel_consumption": np.repeat(input_fuel_cost['fuel_consumption'], end_year_process + 1 - year_process)})
    else:
        fuel_consumption = pd.DataFrame( {"year": years_, "fuel_consumption": np.repeat(0, end_year_process + 1 - year_process)})

    if  (input_fuel_cost["elec_cons"] not in ['', 'nan',  np.nan, None]):
        elec_cons = pd.DataFrame({"year": years_, "elec_cons": np.repeat(input_fuel_cost['elec_cons'], end_year_process + 1 - year_process)})
    else:
        elec_cons = pd.DataFrame( {"year": years_, "elec_cons": np.repeat(0, end_year_process + 1 - year_process)})

    if  (input_fuel_cost["hydrogen_consumption"] not in ['', 'nan',  np.nan, None]):
        hydrogen_consumption = pd.DataFrame({"year": years_, "hydrogen_consumption": np.repeat(input_fuel_cost['hydrogen_consumption'], end_year_process + 1 - year_process)})
    else:
        hydrogen_consumption = pd.DataFrame( {"year": years_, "hydrogen_consumption": np.repeat(0, end_year_process + 1 - year_process)})

    if  (input_fuel_cost["adblue_consumption"] not in ['', 'nan',  np.nan, None]):
        adblue_consumption = pd.DataFrame({"year": years_, "adblue_consumption": np.repeat(input_fuel_cost['adblue_consumption'], end_year_process + 1 - year_process)})
    else:
        adblue_consumption = pd.DataFrame( {"year": years_, "adblue_consumption": np.repeat(0, end_year_process + 1 - year_process)})

    data_frames = [fuel_price, fuel_consumption, impact_seven, adblue_price, adblue_consumption, hydrogen_price, hydrogen_consumption,
                   elec_price, elec_cons]
    df_merged = reduce(lambda left, right: pd.merge(left, right, on=['year'],
                                                    how='outer'), data_frames)
    
    df_merged.fillna(0, inplace=True)

    df_merged['fuel_cost'] = df_merged.apply(lambda x : (x['fuel_consumption'] + (x['fuel_consumption'] * x['extra_fuel_consumption'] / 100) ) * (x['fuel_price'] +x['adblue_price'] * (x['adblue_consumption'] / 100) ) + (x["hydrogen_consumption"] * x["hydrogen_price"]) + (x['elec_price'] * x["elec_cons"]), axis=1)

    return df_merged




#
#lDf_bis = []
#for i in range(input_fuel_df.shape[0]): 
#  df_bis = calculate_fuel_cost(input_fuel_df.iloc[i, :].to_dict(), euro_seven, eng_price_evol)
#  df_bis['powertrain_type'] = input_fuel_df.iloc[i, :].to_dict()['powertrain_type']
#  df_bis['region'] = input_fuel_df.iloc[i, :].to_dict()['region']
#  lDf_bis.append(df_bis)
#
#dfs = pd.concat(lDf_bis)
#dfs.to_csv("data/output/fuel_cost_output.csv", index=False)
#  

