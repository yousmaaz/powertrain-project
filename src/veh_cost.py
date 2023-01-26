import pandas as pd
import numpy as np
from functools import reduce
import numpy_financial as npf

input_veh_price = [

 {
    "powertrain_type": "ICE-G",
    "region": "western europe",
    "fuel_type": "Gasoline",
    "base_vehicle":20000,
    "driveline": 6800,
    "storage_cng" : None,
    "indicator_euro_impact_veh_cost":True,
    "storage_capicity": None,
    "storage_cost": None,
    "battery_capacity": None,
    "battery_cost": None,
    "indicator_fuel_cell": False,
    "fuel_cell_capcity": None,
    "fuel_cell_cost": None,
    "electronics_units":None,
    "charging_point":None,
    "indicator_subsidies": False,
    "subsidies_rate": None,
    "subsidies_year": None,
    "financial_rate":2,
    "residual_rate": 30,
    "year_amortization": 5


 },
{
    "powertrain_type": "ICE-D",
    "region": "western europe",
    "fuel_type": "Diesel",
    "base_vehicle": 20000,
    "driveline": 8800,
    "storage_cng" : None,
    "indicator_euro_impact_veh_cost": True,
    "storage_capicity": None,
    "storage_cost": None,
    "battery_capacity": None,
    "battery_cost": None,
    "indicator_fuel_cell": False,
    "fuel_cell_capcity": None,
    "fuel_cell_cost": None,
    "electronics_units": None,
    "charging_point": None,
    "indicator_subsidies": False,
    "subsidies_rate": None,
    "subsidies_year": None,
    "financial_rate": 2,
    "residual_rate": 30,
    "year_amortization": 5
},

    {
    "powertrain_type": "CNG",
    "region": "western europe",
    "fuel_type": "CNG",
    "base_vehicle": 20000,
    "driveline": 6800,
    "storage_cng": 1917,
    "indicator_euro_impact_veh_cost": False,
    "storage_capicity": None,
    "storage_cost": None,
    "battery_capacity": None,
    "battery_cost": None,
    "indicator_fuel_cell": False,
    "fuel_cell_capcity": None,
    "fuel_cell_cost": None,
    "electronics_units": None,
    "charging_point": None,
    "indicator_subsidies": False,
    "subsidies_rate": None,
    "subsidies_year": None,
    "financial_rate": 2,
    "residual_rate": 25,
    "year_amortization": 5
    },

    {
        "powertrain_type": "HEV",
        "region": "western europe",
        "fuel_type": "HEV",
        "base_vehicle": 20000,
        "driveline": 8300,
        "storage_cng" : None,
        "indicator_euro_impact_veh_cost": True,
        "storage_capicity": None,
        "storage_cost": None,
        "battery_capacity": 2,
        "battery_cost": 220,
        "indicator_fuel_cell": False,
        "fuel_cell_capcity": None,
        "fuel_cell_cost": None,
        "electronics_units": 20,
        "charging_point": None,
        "indicator_subsidies": False,
        "subsidies_rate": None,
        "subsidies_year": None,
        "financial_rate": 2,
        "residual_rate": 30,
        "year_amortization": 5
    },

    {
        "powertrain_type": "PHEV",
        "region": "western europe",
        "fuel_type": "PHEV",
        "base_vehicle": 20000,
        "driveline": 10800,
        "storage_cng" : None,
        "indicator_euro_impact_veh_cost": True,
        "storage_capicity": None,
        "storage_cost": None,
        "battery_capacity": 8,
        "battery_cost": 220,
        "indicator_fuel_cell": False,
        "fuel_cell_capcity": None,
        "fuel_cell_cost": None,
        "electronics_units": 80,
        "charging_point": 1500,
        "indicator_subsidies": True,
        "subsidies_rate": 0.5,
        "subsidies_year": 6,
        "financial_rate": 2,
        "residual_rate": 30,
        "year_amortization": 5
    },

    {
        "powertrain_type": "BEV",
        "region": "western europe",
        "fuel_type": None,
        "base_vehicle": 20000,
        "driveline": 7500,
        "storage_cng" : None,
        "indicator_euro_impact_veh_cost": False,
        "storage_capicity": None,
        "storage_cost": None,
        "battery_capacity": 55,
        "battery_cost": 220,
        "indicator_fuel_cell": False,
        "fuel_cell_capcity": None,
        "fuel_cell_cost": None,
        "electronics_units": 80,
        "charging_point": 1500,
        "indicator_subsidies": True,
        "subsidies_rate": 0.75,
        "subsidies_year": 6,
        "financial_rate": 2,
        "residual_rate": 42,
        "year_amortization": 5
    },

    {
        "powertrain_type": "FCEV",
        "region": "western europe",
        "fuel_type": None,
        "base_vehicle": 20000,
        "driveline": 3500,
        "storage_cng" : None,
        "indicator_euro_impact_veh_cost": False,
        "storage_capicity": 6,
        "storage_cost": 500,
        "battery_capacity": 8,
        "battery_cost": 220,
        "indicator_fuel_cell": True,
        "fuel_cell_capcity": 75,
        "fuel_cell_cost": 300,
        "electronics_units": 80,
        "charging_point": None,
        "indicator_subsidies": True,
        "subsidies_rate": 1,
        "subsidies_year": 9,
        "financial_rate": 2,
        "residual_rate": 40,
        "year_amortization": 5
    }

]

from collections import defaultdict
my_dict = defaultdict(list)

for dic in input_veh_price:
    for key, value in dic.items():
        my_dict[key].append(value)

df_input_veh_price=pd.DataFrame(my_dict)

def get_euro_seven_impact(input_veh_price, euro_seven_input):
    # TODO Check if fuel_type exists before filtering

    request = (euro_seven_input['region'] == input_veh_price['region']) & (euro_seven_input['fuel_type'] == input_veh_price['fuel_type'])

    return euro_seven_input.loc[request, ["year","depollution_veh_cost"]].reset_index(drop=True)


def calculate_electronic_euro_kw(input_veh_price, other_data, year_calcul=2021):
    # TODO set a global variables to name of type other data
    electronic_data = other_data.loc[(other_data['type'] == 'Electronics') & (other_data['region'] == input_veh_price['region']), :].reset_index(drop=True)

    start_index = electronic_data.index[electronic_data['year'] == year_calcul].tolist()[0]

    for i in range(start_index, len(electronic_data)):
        if electronic_data.loc[i, 'year'] == year_calcul:
            electronic_data.loc[i, "electronic_value"] = input_veh_price['electronics_units'] * (1 + (electronic_data.loc[i,"value"] / 100) )
        elif (electronic_data.loc[i, 'year'] >= year_calcul):
            electronic_data.loc[i, "electronic_value"] = electronic_data.loc[i-1, "electronic_value"] *  (1 + (electronic_data.loc[i, "value"] / 100) )
        else:
            electronic_data.loc[i, "electronic_value"] =0


    return electronic_data[['year', 'electronic_value']]

def calculate_electronic_euro(input_veh_price, electronic_euro_kw):

    if input_veh_price['indicator_fuel_cell']:
        electronic_euro_kw['electronic_euro'] = electronic_euro_kw['electronic_value'].values * (input_veh_price['battery_capacity'] +   input_veh_price['fuel_cell_capcity'])
    else:
        electronic_euro_kw['electronic_euro'] = electronic_euro_kw['electronic_value'].values * input_veh_price['battery_capacity']

    return electronic_euro_kw[['year','electronic_euro']]

def cost_battery(input_veh_price, other_data, year_calcul=2021):

    battery_price_evol=other_data.loc[(other_data['region'] == input_veh_price['region']) & (other_data['type'] == 'Battery cost evolution'), :].reset_index(drop=True)

    start_index = battery_price_evol.index[battery_price_evol['year'] == year_calcul].tolist()[0]

    for i in range(start_index, len(battery_price_evol)):
        if battery_price_evol.loc[i, 'year'] == year_calcul:
            battery_price_evol.loc[i, "battery_cost"] = input_veh_price['battery_cost']

        elif (battery_price_evol.loc[i, 'year'] >= year_calcul):
            battery_price_evol.loc[i, "battery_cost"] = battery_price_evol.loc[i-1, "battery_cost"] * (1 + (battery_price_evol.loc[i-1, "value"] / 100))
        else:
            battery_price_evol.loc[i, "battery_cost"] = 0

    return battery_price_evol[['year', 'battery_cost']]

def battery_total_cost(input_veh_price, cost_battery, electronic_euro):

    cost_battery_elec = pd.merge(cost_battery, electronic_euro, on="year", how="inner")

    if input_veh_price['indicator_fuel_cell']:
        cost_battery_elec["battery_total"] = cost_battery_elec['battery_cost'] * input_veh_price['battery_capacity']
    else:
        cost_battery_elec["battery_total"] = cost_battery_elec['battery_cost'] * input_veh_price['battery_capacity'] - cost_battery_elec['electronic_euro']

    return cost_battery_elec[['year', 'battery_total']]

def fuell_cell_cost(input_veh_price, other_data, year_calcul=2021):
    fcev_price_evol = other_data.loc[(other_data['region'] == input_veh_price['region']) & (
                other_data['type'] == 'FCEV Price evolution'), :].reset_index(drop=True)

    start_index = fcev_price_evol.index[fcev_price_evol['year'] == year_calcul].tolist()[0]

    for i in range(start_index, len(fcev_price_evol)):
        if fcev_price_evol.loc[i, 'year'] == year_calcul:
            fcev_price_evol.loc[i, "fuel_cell_cost"] = input_veh_price['fuel_cell_cost']

        elif (fcev_price_evol.loc[i, 'year'] >= year_calcul):
            fcev_price_evol.loc[i, "fuel_cell_cost"] = fcev_price_evol.loc[i - 1, "fuel_cell_cost"] * (
                        1 + (fcev_price_evol.loc[i-1, "value"] / 100))
        else:
            fcev_price_evol.loc[i, "fuel_cell_cost"] = 0

    return fcev_price_evol[['year', 'fuel_cell_cost']]

def fuell_cell_total_cost(input_veh_price, fuel_cell_cost, electronic_euro):

    fuel_cell_elec = pd.merge(fuel_cell_cost, electronic_euro, on="year", how="inner")
    fuel_cell_elec["fuel_cell_total"] = fuel_cell_elec['fuel_cell_cost'] * input_veh_price['fuel_cell_capcity'] - fuel_cell_elec['electronic_euro']
    return fuel_cell_elec[['year', 'fuel_cell_total']]

def calculate_storage_cost(input_veh_price, other_data, year_calcul=2021):
    h2_storage_evol = other_data.loc[(other_data['region'] == input_veh_price['region']) & (
            other_data['type'] == 'Hydrogen storage'), :].reset_index(drop=True)

    start_index = h2_storage_evol.index[h2_storage_evol['year'] == year_calcul].tolist()[0]

    for i in range(start_index, len(h2_storage_evol)):
        if h2_storage_evol.loc[i, 'year'] == year_calcul:
            h2_storage_evol.loc[i, "storage_cost"] = input_veh_price['storage_cost']

        elif (h2_storage_evol.loc[i, 'year'] >= year_calcul):
            h2_storage_evol.loc[i, "storage_cost"] = h2_storage_evol.loc[i - 1, "storage_cost"] * (
                    1 + (h2_storage_evol.loc[i-1, "value"] / 100))
        else:
            h2_storage_evol.loc[i, "storage_cost"] = 0

    h2_storage_evol['storage_total'] = input_veh_price['storage_capicity'] * h2_storage_evol['storage_cost']

    return h2_storage_evol[['year', 'storage_total']]

def calculate_subsidies(input_veh_price, subsidies, year_calcul=2021):

    subsidies_filter = subsidies.loc[(subsidies['region'] == input_veh_price['region']), :].reset_index(drop=True)

    subsidies_filter['subsidies'] = np.where(subsidies_filter['year'] <= year_calcul + input_veh_price['subsidies_year'],  input_veh_price['subsidies_rate'], 0) * subsidies_filter["value"]

    return subsidies_filter[['year', 'subsidies']]





euro_seven = pd.read_csv("data/euro_seven_impact.csv")

other_data=pd.read_csv("data/other_data.csv")

subsidies_data = pd.read_csv("data/subsidies_data.csv")




def veh_price_claculation(input_veh_price, euro_seven_impact, other_data, subsidies, year_process=2021, end_year_process=2040):

    #TODO ADD verification for end_year_process to be same as economic impact data

    years_ = range(year_process, end_year_process+1)

    if input_veh_price["base_vehicle"] is not None:
        base_vehicle = pd.DataFrame({"year": years_ , "base_vehicle" : np.repeat(input_veh_price["base_vehicle"], end_year_process + 1 - year_process)})
    else:
        base_vehicle = pd.DataFrame({"year": years_ , "base_vehicle" : np.repeat(0, end_year_process + 1 - year_process)})

    if input_veh_price["driveline"] is not None:
        driveline = pd.DataFrame({"year": years_ , "driveline" : np.repeat(input_veh_price["driveline"], end_year_process + 1 - year_process)})
    else:
        driveline = pd.DataFrame({"year": years_ , "driveline" : np.repeat(0, end_year_process + 1 - year_process)})

    if input_veh_price["charging_point"] is not None:
        charg_point_input =  pd.DataFrame({"year": years_ , "charging_point" : np.repeat(input_veh_price["charging_point"] , end_year_process + 1 - year_process)})
    else:
        charg_point_input = pd.DataFrame({"year": years_ , "charging_point" : np.repeat(0 , end_year_process + 1 - year_process)})


    if input_veh_price['storage_cng'] is not None:
        storage_cng =  pd.DataFrame({"year": years_ , "storage_cng" : np.repeat(input_veh_price["storage_cng"] , end_year_process + 1 - year_process)})
    else:
        storage_cng = pd.DataFrame({"year": years_ , "storage_cng" : np.repeat(0 , end_year_process + 1 - year_process)})


    if input_veh_price["indicator_euro_impact_veh_cost"]:
        euro_seven_impact_value = get_euro_seven_impact(input_veh_price,euro_seven_impact)
    else:
        euro_seven_impact_value = pd.DataFrame({"year": years_, "depollution_veh_cost": np.repeat(0, end_year_process + 1 - year_process)})


    if input_veh_price["electronics_units"] is not None:
        elec_euro_kw = calculate_electronic_euro_kw(input_veh_price, other_data, year_process)
        elec_euro = calculate_electronic_euro(input_veh_price, elec_euro_kw)
    else:
        elec_euro = pd.DataFrame({"year": years_,  "electronic_euro" : np.repeat(0, end_year_process + 1 - year_process)})


    if input_veh_price['battery_cost'] is not None:
        bat_cost = cost_battery(input_veh_price, other_data, year_process)
        bat_tot = battery_total_cost(input_veh_price, bat_cost, elec_euro)
    else:
        bat_tot = pd.DataFrame({"year": years_, "battery_total": np.repeat(0, end_year_process + 1 - year_process)})


    if input_veh_price['fuel_cell_capcity'] is not None:
        fuel_cell_cost = fuell_cell_cost(input_veh_price, other_data)
        fuel_cell_cost_tot = fuell_cell_total_cost(input_veh_price, fuel_cell_cost, elec_euro)
    else:
        fuel_cell_cost_tot = pd.DataFrame({"year": years_, "fuel_cell_total": np.repeat(0, end_year_process + 1 - year_process)})


    if input_veh_price['storage_cost'] is not None:
        storage_cost_tot = calculate_storage_cost(input_veh_price, other_data)
    else:
        storage_cost_tot = pd.DataFrame({"year": years_, "storage_total": np.repeat(0, end_year_process + 1 - year_process)})


    if input_veh_price["indicator_subsidies"]:
        subsidies_df = calculate_subsidies(input_veh_price, subsidies)
    else:
        subsidies_df = pd.DataFrame({"year": years_, "subsidies": np.repeat(0, end_year_process + 1 - year_process)})


    data_frames = [base_vehicle, driveline, charg_point_input, storage_cng, euro_seven_impact_value, elec_euro, bat_tot, fuel_cell_cost_tot, storage_cost_tot, subsidies_df]

    df_merged = reduce(lambda left, right: pd.merge(left, right, on=['year'],
                                                    how='outer'), data_frames)

    df_merged['veh_price'] = df_merged.loc[:, list(set(df_merged.columns).difference(["year"]))].sum(axis=1)

    return df_merged




def calculate_veh_cost(input_veh_price, veh_price_df):

    veh_cost_df = veh_price_df.copy()

    if (input_veh_price['financial_rate'] is not None) & (input_veh_price['residual_rate'] is not None) & (input_veh_price['year_amortization'] is not None):

        veh_cost_df['veh_cost'] = veh_cost_df['veh_price'].apply(lambda x: npf.pmt(input_veh_price['financial_rate'] / 100, input_veh_price['year_amortization'], -x, (input_veh_price['residual_rate'] / 100) * x, 0  ))
    else:
        veh_cost_df['veh_cost'] = None

    return veh_cost_df





df_ = pd.DataFrame()
lDf = []

for i in range(7):
    df = veh_price_claculation(input_veh_price[i], euro_seven, other_data, subsidies_data)
    df_ = calculate_veh_cost(input_veh_price[i], df)
    df_['powertrain_type'] = input_veh_price[i]['powertrain_type']
    df_['region'] = input_veh_price[i]['region']
    lDf.append(df_)

dfs = pd.concat(lDf)
dfs.to_csv("data/output/veh_cost_output.csv", index=False)















