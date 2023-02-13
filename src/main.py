import streamlit as st
from fuel_cost import * 
from veh_cost import * 
from TCO import * 
from ihs import * 
from MS import * 

@st.cache(allow_output_mutation=True)
def load_assmption_data():
    euro_seven     = pd.read_csv("data/euro_seven_impact.csv")
    eng_price_evol = pd.read_csv("data/energy_price_evolution.csv")
    other_data     = pd.read_csv("data/other_data.csv")
    subsidies_data = pd.read_csv("data/subsidies_data.csv")
    ihs = pd.read_csv("data/ihs-202302.csv")
    quartiles= pd.read_csv("data/population_quartile.csv")
    
    return euro_seven, eng_price_evol, other_data, subsidies_data, ihs, quartiles

if __name__ == '__main__':

  st.title(f"Mix Powertrain Apps")
  
  
  euro_seven, eng_price_evol, other_data, subsidies_data, ihs, quartiles = load_assmption_data()
  
  file_fuel = st.sidebar.file_uploader("upload fuel cost input file", type={"csv"})
  if file_fuel is not None:
      input_fuel_df = pd.read_csv(file_fuel)
  else:
      st.error("Need fuel cost input file to run application ")
      
  
  veh_price_file = st.sidebar.file_uploader("upload veh price input file", type={"csv"})
  if file_fuel is not None:
      input_veh_price = pd.read_csv(veh_price_file)
  else:
      st.error("Need veh price input file to run application ")
      
  rate_input_file = st.sidebar.file_uploader("upload rate input file", type={"csv"})
  if file_fuel is not None:
      input_rate = pd.read_csv(rate_input_file)
  else:
      st.error("Need rate input file to run application ")
  
  
  year_start=st.sidebar.slider('What is your begin year of calcul', min_value=2023, max_value=2030, value=2023, step=1)
  year_end=st.sidebar.slider('What is your end year of calcul', min_value=2023, max_value=2030, value=2030, step=1)
  
  if st.sidebar.button('run application'):
      
    lDf_bis = []
    for i in range(input_fuel_df.shape[0]): 
      df_bis = calculate_fuel_cost(input_fuel_df.iloc[i, :].to_dict(), euro_seven, eng_price_evol, year_process=year_start-2, end_year_process=year_end)
      df_bis = df_bis.loc[(df_bis.year >= year_start-2) & (df_bis.year <= year_end), :].reset_index()
      df_bis['powertrain_type'] = input_fuel_df.iloc[i, :].to_dict()['powertrain_type']
      df_bis['region'] = input_fuel_df.iloc[i, :].to_dict()['region']
      lDf_bis.append(df_bis)

    output_fuel_cost = pd.concat(lDf_bis)
    st.dataframe(output_fuel_cost)
    output_fuel_cost.to_csv("data/output/fuel_cost_output.csv", index=False)

    df_ = pd.DataFrame()
    lDf = []

    for i in range(7):
      df = veh_price_claculation(input_veh_price.iloc[i, :].to_dict(), euro_seven, other_data, subsidies_data, year_process=year_start-2, end_year_process=year_end)
      df_ = calculate_veh_cost(input_veh_price.iloc[i, :].to_dict(), df)
      df_['powertrain_type'] = input_veh_price.iloc[i, :].to_dict()['powertrain_type']
      df_['region'] = input_veh_price.iloc[i, :].to_dict()['region']
      lDf.append(df_)

    output_veh_cost = pd.concat(lDf)
    st.dataframe(output_veh_cost)
    output_veh_cost.to_csv("data/output/veh_cost_output.csv", index=False)
    
    
    TCO = calculate_TCO(output_fuel_cost, output_veh_cost, input_rate, quartiles)
    st.dataframe(TCO)
    
    agg_volume_powertrain_per = get_volumes_ihs(ihs)
    tco_data = get_ms_data(agg_volume_powertrain_per,output_veh_cost, TCO)
    st.dataframe(tco_data)
    
    
    vol = tco_data[tco_data['year'] == year_start][['powertrain_type', 'year', 'region', 'ratio_volume']].rename(columns={'ratio_volume': 'base_volume'})

    tco_data_preview = pd.merge(tco_data, vol, on = ['powertrain_type', 'region'])\
    .query("year_x >= year_y").drop(['year_y'], axis = 1)\
    .rename(columns={'year_x': 'year'})

    
    tco_data_preview["actual_volume"] =np.where(tco_data_preview['year'] == year_start, tco_data_preview["base_volume"], tco_data_preview["base_volume"] + tco_data_preview["s3_ms_normalize_var"]) 
    tco_data_preview["s3_ms_normalize_var"] =np.where(tco_data_preview['year'] == year_start, np.nan, tco_data_preview["s3_ms_normalize_var"]) 

    
    st.dataframe(tco_data_preview[['powertrain_type', 'year', 'region', 'ratio_volume', 'actual_volume', 's3_ms_normalize_var']])

  
  
  
  
