import pandas as pd



#fuel_cost = pd.read_csv("data/output/fuel_cost_output.csv")
#veh_cost = pd.read_csv("data/output/veh_cost_output.csv")
#input_rate = pd.read_csv("data/input_rate.csv")

def calculate_insurance(veh_cost, insurance_rate):
    veh_cost_filter = veh_cost.loc[(veh_cost['powertrain_type'] == insurance_rate['powertrain_type']) & (veh_cost['region'] == insurance_rate['region']), :].reset_index(drop=True)
    veh_cost_filter['insurance_euro'] = veh_cost_filter['veh_price'] * insurance_rate['insurance_rate'] / 100
    veh_cost_filter['mr_euro'] = veh_cost_filter['veh_price'] * insurance_rate['mr_rate'] / 100
    return veh_cost_filter


def calculate_TCO(fuel_cost, veh_cost, input_rate, quartiles):
  veh_cost_insurance = pd.concat([calculate_insurance(veh_cost, input_rate.iloc[i, :].to_dict()) for i in range(7)])

  alldata = pd.merge(fuel_cost, veh_cost_insurance, on=["powertrain_type", "region", "year"])

#  quartiles= pd.read_csv("data/population_quartile.csv")

  df = pd.merge(alldata[['powertrain_type', 'region', 'year', 'veh_cost', 'fuel_cost', 'insurance_euro', 'mr_euro']], quartiles, on=['year', 'region'])


  df['TCO'] = (df['veh_cost'] + df['insurance_euro'] + df['mr_euro']) / df['km'] + (df['fuel_cost'] / 100)

  df['TCO_percent'] = df['TCO'] * df['value'] / 100
  
  return df 

#  df.to_csv("data/output/TCO.csv", index=False)


