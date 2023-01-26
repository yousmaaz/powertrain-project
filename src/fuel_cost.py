import pandas as pd
import numpy as np
from functools import reduce
import numpy_financial as npf

input_fuel_cost = [

    {
        "powertrain_type": "ICE-G",
        "region": "western europe",
        "fuel_type": "Gasoline",
        "fuel_price": 1.35,
        "fuel_consumption": 5.5,
        "indicator_euro_seven_impact_fuel": True,
        "elec_cons": None,
        "elec_price": None,
        "hydrogen_price": None,
        "hydrogen_consumption": None,
        "indicator_abdule": False,
        "adblue_consumption": None,
        "adblue_price": None

    },
    {
        "powertrain_type": "ICE-D",
        "region": "western europe",
        "fuel_type": "Diesel",
        "fuel_price": 1.15,
        "fuel_consumption": 4.4,
        "indicator_euro_seven_impact_fuel": True,
        "elec_cons": None,
        "elec_price": None,
        "hydrogen_price": None,
        "hydrogen_consumption": None,
        "indicator_abdule": True,
        "adblue_consumption": 6,
        "adblue_price": 2

    },
    {
        "powertrain_type": "CNG",
        "region": "western europe",
        "fuel_type": "CNG",
        "fuel_price": 0.7,
        "fuel_consumption": 7.2,
        "indicator_euro_seven_impact_fuel": False,
        "elec_cons": None,
        "elec_price": None,
        "hydrogen_price": None,
        "hydrogen_consumption": None,
        "indicator_abdule": False,
        "adblue_consumption": None,
        "adblue_price": None

    },
    {
        "powertrain_type": "HEV",
        "region": "western europe",
        "fuel_type": "Gasoline",
        "fuel_price": 1.35,
        "fuel_consumption": 5,
        "indicator_euro_seven_impact_fuel": True,
        "elec_cons": None,
        "elec_price": None,
        "hydrogen_price": None,
        "hydrogen_consumption": None,
        "indicator_abdule": False,
        "adblue_consumption": None,
        "adblue_price": None

    },
    {
        "powertrain_type": "PHEV",
        "region": "western europe",
        "fuel_type": "Gasoline",
        "fuel_price": 1.35,
        "fuel_consumption": 2,
        "indicator_euro_seven_impact_fuel": False,
        "elec_cons": 10,
        "elec_price": 0.15,
        "hydrogen_price": None,
        "hydrogen_consumption": None,
        "indicator_abdule": False,
        "adblue_consumption": None,
        "adblue_price": None

    },
    {
        "powertrain_type": "BEV",
        "region": "western europe",
        "fuel_type": None,
        "fuel_price": None,
        "fuel_consumption": None,
        "indicator_euro_seven_impact_fuel": False,
        "elec_cons": 15,
        "elec_price": 0.15,
        "hydrogen_price": None,
        "hydrogen_consumption": None,
        "indicator_abdule": False,
        "adblue_consumption": None,
        "adblue_price": None

    },
    {
        "powertrain_type": "FCEV",
        "region": "western europe",
        "fuel_type": None,
        "fuel_price": None,
        "fuel_consumption": None,
        "indicator_euro_seven_impact_fuel": False,
        "elec_cons": 15,
        "elec_price": 0.15,
        "hydrogen_price": 6,
        "hydrogen_consumption": 1,
        "indicator_abdule": False,
        "adblue_consumption": None,
        "adblue_price": None

    },


]

euro_seven = pd.read_csv("data/euro_seven_impact.csv")
eng_price_evol = pd.read_csv("data/energy_price_evolution.csv")

def get_euro_seven_impact_fuel(input_fuel_cost, euro_seven_input):
    # TODO Check if fuel_type exists before filtering


    request = (euro_seven_input['region'] == input_fuel_cost['region']) & (euro_seven_input['fuel_type'] == input_fuel_cost['fuel_type'])

    euro_seven_value = euro_seven_input.loc[request, ["year","extra_fuel_consumption"]].reset_index(drop=True)


    return euro_seven_value

def calculate_fuel_price(input_fuel_cost, eng_price_evol, year_calcul=2021):

    fuel_evol = eng_price_evol.loc[(eng_price_evol['region'] == input_fuel_cost['region']) & (
            eng_price_evol['energie_type'] == input_fuel_cost['fuel_type']), :].reset_index(drop=True)

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

    print(f"elec_evol => {elec_evol}")
    print(f"index => {elec_evol.index[elec_evol['year'] == year_calcul].tolist()}")

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

    if input_fuel_cost["fuel_type"] is not None:
        fuel_price = calculate_fuel_price(input_fuel_cost, eng_price_evol, year_calcul=year_process)
    else:
        fuel_price = pd.DataFrame({"year": years_ , "fuel_price" : np.repeat(0, end_year_process + 1 - year_process)})

    if input_fuel_cost["indicator_euro_seven_impact_fuel"]:
        impact_seven = get_euro_seven_impact_fuel(input_fuel_cost, euro_seven)
    else:
        impact_seven = pd.DataFrame({"year": years_ , "extra_fuel_consumption" : np.repeat(0, end_year_process + 1 - year_process)})

    if input_fuel_cost["elec_price"] is not None:
        elec_price = calculate_elec_price(input_fuel_cost, eng_price_evol, year_calcul=year_process)
    else:
        elec_price = pd.DataFrame({"year": years_ , "elec_price" : np.repeat(0, end_year_process + 1 - year_process)})

    if input_fuel_cost["hydrogen_price"] is not None:
        hydrogen_price = calculate_hydrogen_price(input_fuel_cost, eng_price_evol, year_calcul=year_process)
    else:
        hydrogen_price = pd.DataFrame({"year": years_ , "hydrogen_price" : np.repeat(0, end_year_process + 1 - year_process)})

    if input_fuel_cost["adblue_price"] is not None:
        adblue_price = calculate_adblue_price(input_fuel_cost, eng_price_evol, year_calcul=year_process)
    else:
        adblue_price = pd.DataFrame({"year": years_ , "adblue_price" : np.repeat(0, end_year_process + 1 - year_process)})

    if input_fuel_cost['fuel_consumption'] is not None:
        fuel_consumption = pd.DataFrame({"year": years_, "fuel_consumption": np.repeat(input_fuel_cost['fuel_consumption'], end_year_process + 1 - year_process)})
    else:
        fuel_consumption = pd.DataFrame( {"year": years_, "fuel_consumption": np.repeat(0, end_year_process + 1 - year_process)})

    if input_fuel_cost['elec_cons'] is not None:
        elec_cons = pd.DataFrame({"year": years_, "elec_cons": np.repeat(input_fuel_cost['elec_cons'], end_year_process + 1 - year_process)})
    else:
        elec_cons = pd.DataFrame( {"year": years_, "elec_cons": np.repeat(0, end_year_process + 1 - year_process)})

    if input_fuel_cost['hydrogen_consumption'] is not None:
        hydrogen_consumption = pd.DataFrame({"year": years_, "hydrogen_consumption": np.repeat(input_fuel_cost['hydrogen_consumption'], end_year_process + 1 - year_process)})
    else:
        hydrogen_consumption = pd.DataFrame( {"year": years_, "hydrogen_consumption": np.repeat(0, end_year_process + 1 - year_process)})

    if input_fuel_cost['adblue_consumption'] is not None:
        adblue_consumption = pd.DataFrame({"year": years_, "adblue_consumption": np.repeat(input_fuel_cost['adblue_consumption'], end_year_process + 1 - year_process)})
    else:
        adblue_consumption = pd.DataFrame( {"year": years_, "adblue_consumption": np.repeat(0, end_year_process + 1 - year_process)})

    data_frames = [fuel_price, fuel_consumption, impact_seven, adblue_price, adblue_consumption, hydrogen_price, hydrogen_consumption,
                   elec_price, elec_cons]

    df_merged = reduce(lambda left, right: pd.merge(left, right, on=['year'],
                                                    how='outer'), data_frames)

    df_merged['fuel_cost'] = df_merged.apply(lambda x : (x['fuel_consumption'] + (x['fuel_consumption'] * x['extra_fuel_consumption'] / 100) ) * (x['fuel_price'] +x['adblue_price'] * (x['adblue_consumption'] / 100) ) + (x["hydrogen_consumption"] * x["hydrogen_price"]) + (x['elec_price'] * x["elec_cons"]), axis=1)

    return df_merged

df_ = pd.DataFrame()
lDf = []
for i in range(7):

    df_ = calculate_fuel_cost(input_fuel_cost[i], euro_seven, eng_price_evol)
    df_['powertrain_type'] = input_fuel_cost[i]['powertrain_type']
    df_['region'] = input_fuel_cost[i]['region']
    lDf.append(df_)

dfs = pd.concat(lDf)
dfs.to_csv("data/output/fuel_cost_output.csv", index=False)



