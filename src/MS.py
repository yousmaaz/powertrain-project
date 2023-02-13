import pandas as pd
import numpy as np
import math

#veh_cost = pd.read_csv('data/output/veh_cost_output.csv')
#tco_data = pd.read_csv('data/output/TCO.csv')
#agg_volume_powertrain_per = pd.read_csv("data/output/ihs_volume_output.csv")
def calculate_competitveness_factor(row, factor=2): 
    if (math.isnan(row['TCO_VAR']) == False): 
        A = row['TCO_AVG'] - row['TCO_MIN']
        B = row['TCO_AVG_POWERTRAIN'] - row['TCO_MIN']
        F = row['TCO_AVG'] / factor
        
        return np.exp(0.5 * (A / F)**2) * np.exp(-0.5 * (B / F)**2)
    else: 
        return np.nan
    
def calculate_veh_cot_factor(row, factor=1.5): 
    try:
        if (math.isnan(row['veh_price_ihs_avg_previous']) == False): 
            A = row['veh_price_ihs_avg_previous'] - row['veh_price_km_min']
            B = row['veh_price_km'] - row['veh_price_km_min']
            F = row['veh_price_ihs_avg_previous'] / factor

            return np.exp(0.5 * (A / F)**2) * np.exp(-0.5 * (B / F)**2)
        else: 
            return np.nan
    except: 
        return np.nan
      
def s3_correction_market_share(row):
    try: 
        if ((row['ratio_volume_previous'] + row["s2_ms_normalize_var"]) < 0): 
            return 0

        elif ((row['ratio_volume_previous'] + row["s2_ms_normalize_var"]) > 1):
            return 1-row['ratio_volume_previous'] 
        else: 
            return row["s2_ms_normalize_var"]
    except: 
        return np.nan

def s2_correction_market_share(row):
    try: 
        if ((row['ratio_volume_previous'] + row["s1_ms_normalize_var"]) < 0): 
            return -row['ratio_volume_previous'] / 2

        elif ((row['ratio_volume_previous'] + row["s1_ms_normalize_var"]) > 1):
            return 1-row['ratio_volume_previous'] 
        else: 
            return row["s1_ms_normalize_var"]
    except: 
        return np.nan
    
def s1_correction_market_share(row):
    try: 
        if ((row['ratio_volume_previous'] + row["s1_variation_factor"]) < 0): 
            return -row['ratio_volume_previous'] 

        elif ((row['ratio_volume_previous'] + row["s1_variation_factor"]) > 1):
            return 1-row['ratio_volume_previous'] 
        else: 
            return row["s1_variation_factor"]
    except: 
        return np.nan

def get_ms_data(agg_volume_powertrain_per,veh_cost, tco_data):
  
  tco_data = pd.merge(tco_data, 
                      veh_cost[['powertrain_type', 'region', 'year', 'veh_price']],
                      on = ['powertrain_type', 'region', 'year'])



  tco_data = pd.merge(tco_data, 
                      agg_volume_powertrain_per[['powertrain_type', 'region', 'year', 'ratio_volume']],
                      on = ['powertrain_type', 'region', 'year'], how="left")

  tco_data['ratio_volume'] = tco_data['ratio_volume'].fillna(0)

  tco_data['TCO_AVG_POWERTRAIN'] = tco_data.groupby(['region', 'year','powertrain_type'])["TCO_percent"].transform(sum)
  tco_data['TCO_AVG'] = tco_data.groupby(['region', 'year'])["TCO_AVG_POWERTRAIN"].transform(np.mean)
  tco_data['TCO_MIN'] = tco_data.groupby(['region', 'year'])["TCO_AVG_POWERTRAIN"].transform(min)



  tco_data['veh_price_km'] = tco_data['veh_price'] / 1000
  tco_data['veh_price_km_avg'] = tco_data.groupby(['region', 'year'])["veh_price_km"].transform(np.mean)
  tco_data['veh_price_km_min'] = tco_data.groupby(['region', 'year'])["veh_price_km"].transform(min)

  tco_data = tco_data[['powertrain_type', 'region', 'year', 'TCO_AVG_POWERTRAIN', 'TCO_AVG','TCO_MIN', 'veh_price_km','veh_price_km_avg', 'ratio_volume', 'veh_price_km_min']].drop_duplicates()
  tco_data['TCO_VAR'] = tco_data.groupby(['powertrain_type', 'region'])['TCO_AVG_POWERTRAIN'].pct_change() 

  tco_data['veh_price_ihs']= tco_data['veh_price_km'] * tco_data['ratio_volume']
  tco_data['veh_price_ihs_avg'] = tco_data.groupby(['region', 'year'])['veh_price_ihs'].transform(sum)
  s = tco_data[['region', 'year', 'veh_price_ihs_avg']].drop_duplicates()
  s['veh_price_ihs_avg_previous'] = s['veh_price_ihs_avg'].shift(1)
  tco_data = pd.merge(tco_data, s.drop(['veh_price_ihs_avg'], axis=1), on = ['region', 'year'])

  tco_data['TCO_Compet_factor'] = tco_data.apply(lambda x: calculate_competitveness_factor(x, factor = 2), axis=1)
  tco_data['veh_cost_factor'] = tco_data.apply(lambda x: calculate_veh_cot_factor(x, factor = 1.5), axis=1)

  s = tco_data[['region', 'year', 'powertrain_type', 'ratio_volume']].drop_duplicates()
  s['ratio_volume_previous'] = s.groupby(['region','powertrain_type'])['ratio_volume'].shift(1)
  s['ratio_volume_previous_minus'] = s.groupby(['region','powertrain_type'])['ratio_volume'].shift(2)
  tco_data = pd.merge(tco_data, s.drop(['ratio_volume'], axis=1), on = ['region', 'year', 'powertrain_type'])
  tco_data['s1_variation_factor'] = ((- tco_data['veh_cost_factor'] * tco_data['TCO_Compet_factor'] * tco_data['TCO_VAR']) \
                                     + ((tco_data['TCO_Compet_factor'] -1) * tco_data['veh_cost_factor']))\
                                      * (1 - tco_data['ratio_volume_previous'])

  tco_data['s1_market_share_correction'] = tco_data.apply(lambda row : s1_correction_market_share(row), axis=1)

  tco_data["s1_ms_normalize_var"] = tco_data['s1_market_share_correction'] -\
  (tco_data["ratio_volume_previous_minus"] * tco_data.groupby(['region', 'year'])['s1_market_share_correction'].transform(sum))

  tco_data['s2_market_share_correction'] = tco_data.apply(lambda row : s2_correction_market_share(row), axis=1)
  tco_data["s2_ms_normalize_var"] = tco_data['s2_market_share_correction'] -\
  (tco_data["ratio_volume_previous"] * tco_data.groupby(['region', 'year'])['s2_market_share_correction'].transform(sum))

  tco_data['s3_market_share_correction'] = tco_data.apply(lambda row : s3_correction_market_share(row), axis=1)
  tco_data["s3_ms_normalize_var"] = tco_data['s3_market_share_correction'] -\
  (tco_data["ratio_volume_previous"] * tco_data.groupby(['region', 'year'])['s3_market_share_correction'].transform(sum))

  tco_data['ms_normalize_var_cumsum'] = tco_data.groupby(['region','powertrain_type'])['s3_ms_normalize_var'].transform(np.cumsum)
  
  return (tco_data)