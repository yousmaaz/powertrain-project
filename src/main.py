import streamlit as st
from fuel_cost import * 
from veh_cost import * 
from TCO import * 
from ihs import * 
from MS import * 
import plotly.express as px
import plotly.graph_objects as go


def load_assmption_data():
    euro_seven     = pd.read_csv("data/euro_seven_impact.csv")
    eng_price_evol = pd.read_csv("data/energy_price_evolution.csv")
    other_data     = pd.read_csv("data/other_data.csv")
    subsidies_data = pd.read_csv("data/subsidies_data.csv")
    ihs = pd.read_csv("data/ihs-202302.csv")
    quartiles= pd.read_csv("data/population_quartile.csv")
    
    return euro_seven, eng_price_evol, other_data, subsidies_data, ihs, quartiles
  
@st.experimental_memo
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

if __name__ == '__main__':

#  st.title(f"Mix Powertrain Apps")
  
  st.set_page_config(
    page_title="Mix Powertrain Apps",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded")
  
  st.title(f"Mix Powertrain Apps")
  
  euro_seven, eng_price_evol, other_data, subsidies_data, ihs, quartiles = load_assmption_data()
  
  file_fuel = st.sidebar.file_uploader("upload fuel cost input file", type={"csv"})
  veh_price_file = st.sidebar.file_uploader("upload veh price input file", type={"csv"})
  rate_input_file = st.sidebar.file_uploader("upload rate input file", type={"csv"})
  
  if (file_fuel is not None) & (veh_price_file is not None) & (rate_input_file is not None):
      input_fuel_df = pd.read_csv(file_fuel)
      
      input_veh_price = pd.read_csv(veh_price_file)
      
      input_rate = pd.read_csv(rate_input_file)
      
      
      filter_region = st.expander("Do you want to filter by regions ?")
      with filter_region:
        regions = st.sidebar.multiselect('Which region would you like to process on',
                  input_fuel_df.region.unique())

  else:
      st.success("Need input files to run application ")
      

  
  
  year_start=st.sidebar.slider('What is your begin year of calcul', min_value=2023, max_value=2030, value=2023, step=1)
  year_end=st.sidebar.slider('What is your end year of calcul', min_value=2023, max_value=2030, value=2030, step=1)
  
  
  
  
  if st.sidebar.button('run application'):
    
    regions = [region.lower() for region in regions]
    
    col1, col2 = st.columns(2)
    
    with col1:
      st.subheader("Fuel Cost Calculation")
      
      lDf_bis = []
      for i in range(input_fuel_df.shape[0]): 
        df_bis = calculate_fuel_cost(input_fuel_df.iloc[i, :].to_dict(), euro_seven, eng_price_evol, year_process=year_start-2, end_year_process=year_end)
        df_bis = df_bis.loc[(df_bis.year >= year_start-2) & (df_bis.year <= year_end), :].reset_index(drop=True)
        df_bis['powertrain_type'] = input_fuel_df.iloc[i, :].to_dict()['powertrain_type']
        df_bis['region'] = input_fuel_df.iloc[i, :].to_dict()['region']
        lDf_bis.append(df_bis)

      output_fuel_cost = pd.concat(lDf_bis)
      output_fuel_cost = output_fuel_cost.loc[output_fuel_cost.region.isin(regions), :]
      


      
      
      show_data = st.expander("Show me data 👉")
      with show_data:
        st.dataframe(output_fuel_cost)
        csv = convert_df(output_fuel_cost)
        st.download_button(
            "Press to Download",
             csv,
            "file.csv",
            "text/csv",
            key='download-csv-4'
        )
      
      fig = px.line(output_fuel_cost, x='year', y='fuel_cost', color='powertrain_type', facet_col="region", markers=True)
      fig.update_layout(title_text="Evolution Fuel cost by powertrain",
                        title_x=0,margin= dict(l=0,r=30,b=50,t=30), yaxis_title=None, xaxis_title=None)
      fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
      st.plotly_chart(fig, use_container_width=True)
      
      output_fuel_cost.to_csv("data/output/fuel_cost_output.csv", index=False)
    
    with col2:
      st.subheader("Vehicle Cost Calculation")
      df_ = pd.DataFrame()
      lDf = []

      for i in range(input_veh_price.shape[0]):
        df = veh_price_claculation(input_veh_price.iloc[i, :].to_dict(), euro_seven, other_data, subsidies_data, year_process=year_start-2, end_year_process=year_end)
        df_ = calculate_veh_cost(input_veh_price.iloc[i, :].to_dict(), df)
        df_ = df_.loc[(df_.year >= year_start-2) & (df_.year <= year_end), :].reset_index(drop=True)
        df_['powertrain_type'] = input_veh_price.iloc[i, :].to_dict()['powertrain_type']
        df_['region'] = input_veh_price.iloc[i, :].to_dict()['region']
        lDf.append(df_)

      output_veh_cost = pd.concat(lDf)
      output_veh_cost = output_veh_cost.loc[output_veh_cost.region.isin(regions), :]
      
      show_data = st.expander("Show me data 👉")
      with show_data:
        st.dataframe(output_veh_cost)
        csv = convert_df(output_veh_cost)
        st.download_button(
            "Press to Download",
             csv,
            "file.csv",
            "text/csv",
            key='download-csv-3'
        )
      
      fig = px.line(output_veh_cost, x='year', y='veh_cost', color='powertrain_type', facet_col="region", markers=True)
      fig.update_layout(title_text="Evolution Vehicle cost by powertrain",
                        title_x=0,margin= dict(l=0,r=30,b=50,t=30), yaxis_title=None, xaxis_title=None)
      fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
      st.plotly_chart(fig, use_container_width=True)
      output_veh_cost.to_csv("data/output/veh_cost_output.csv", index=False)
      
    col3, col4 = st.columns(2)
    
    with col3:
      st.subheader("Powertrain TCO percentage by quartile/region Calculation")
      TCO = calculate_TCO(output_fuel_cost, output_veh_cost, input_rate, quartiles)
      TCO = TCO.loc[TCO.region.isin(regions), :]
      show_data = st.expander("Show me data 👉")
      with show_data:
        st.dataframe(TCO)
        csv = convert_df(TCO)
        st.download_button(
            "Press to Download",
             csv,
            "file.csv",
            "text/csv",
            key='download-csv-2'
        )
      fig = px.line(TCO, x='year', y='TCO_percent', color='powertrain_type',
                    facet_col="region", facet_row="quartile", markers=True)
      fig.update_layout(title_text="Percentage Powertrain TCO by region and  quartile",
                        yaxis_title=None, xaxis_title=None)
      fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
      
      # hide subplot y-axis titles and x-axis titles
      for axis in fig.layout:
          if type(fig.layout[axis]) == go.layout.YAxis:
              fig.layout[axis].title.text = ''
          if type(fig.layout[axis]) == go.layout.XAxis:
              fig.layout[axis].title.text = ''

      # ensure that each chart has its own y rage and tick labels
      fig.update_yaxes(matches=None, showticklabels=True, visible=True)
      st.plotly_chart(fig, use_container_width=True)
    
    with col4:
      st.subheader("Mean Powertrain TCO percentage by region Calculation")
      agg_volume_powertrain_per = get_volumes_ihs(ihs)
      tco_data = get_ms_data(agg_volume_powertrain_per,output_veh_cost, TCO)
      tco_data = tco_data.loc[TCO.region.isin(regions), :]
      show_data = st.expander("Show me data 👉")
      with show_data:
        st.dataframe(tco_data)
        csv = convert_df(tco_data)
        st.download_button(
            "Press to Download",
             csv,
            "file.csv",
            "text/csv",
            key='download-csv-0'
        )
      
      fig = px.line(tco_data, x='year', y='TCO_AVG_POWERTRAIN', color='powertrain_type',
                    facet_col="region", markers=True)
      fig.update_layout(title_text="Percentage Powertrain TCO by region and  quartile",
                        yaxis_title=None, xaxis_title=None)
      fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
      st.plotly_chart(fig, use_container_width=True)
      
    with st.container():
      st.subheader("Market Share Calculation")
      col1, col2 = st.columns([1, 3])
      
      with col1:
 
        vol = tco_data[tco_data['year'] == year_start][['powertrain_type', 'year', 'region', 'ratio_volume']].rename(columns={'ratio_volume': 'base_volume'})

        tco_data_preview = pd.merge(tco_data, vol, on = ['powertrain_type', 'region'])\
        .query("year_x >= year_y").drop(['year_y'], axis = 1)\
        .rename(columns={'year_x': 'year'})


        tco_data_preview["actual_volume"] =np.where(tco_data_preview['year'] == year_start, tco_data_preview["base_volume"], tco_data_preview["base_volume"] + tco_data_preview["s3_ms_normalize_var"]) 
        tco_data_preview["s3_ms_normalize_var"] =np.where(tco_data_preview['year'] == year_start, np.nan, tco_data_preview["s3_ms_normalize_var"]) 

        s1 = tco_data_preview[['powertrain_type', 'year', 'region', 'ratio_volume', 'actual_volume', 's3_ms_normalize_var']]
        st.dataframe(s1)
        
        csv = convert_df(s1)
        st.download_button(
            "Press to Download",
             csv,
            "file.csv",
            "text/csv",
            key='download-csv-1'
        )
        
      with col2:
        tco_data_preview['ratio_volume'] = tco_data_preview['ratio_volume'].transform(lambda x: x * 100)
       
        fig = px.bar(tco_data_preview, x="year", y="ratio_volume", color="powertrain_type",facet_col="region"
                     , text_auto=True)
        fig.update_layout(title_text="Market Share  by region and powertrain_type from IHS",
                        yaxis_title=None, xaxis_title=None)
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        st.plotly_chart(fig, use_container_width=True)
        
        tco_data_preview['actual_volume'] = tco_data_preview['actual_volume'].transform(lambda x: x * 100)
        fig = px.bar(tco_data_preview, x="year", y="actual_volume", color="powertrain_type",facet_col="region"
                     , text_auto=True)
        fig.update_layout(title_text="Market Share  by region and powertrain_type by Simulation",
                        yaxis_title=None, xaxis_title=None)
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        st.plotly_chart(fig, use_container_width=True)


      

  
  
  
