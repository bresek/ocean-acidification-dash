
from datetime import datetime
import plotly.express as px
import pandas as pd
import os
# import matplotlib
import numpy as np
# import plotly.graph_objects as go


# defining data processing functions
class dataCleaning:
    def folderToDfs(folderpath):
        """returns list of dataframes from an input folder"""
        files = os.listdir(folderpath)
        df_list = []
        for file in files:
            if not file.startswith('.'):
                temp_df = pd.read_csv(folderpath+'/'+file)
                df_list.append(temp_df)
        return df_list

    def renameCols(dfs, colNames):
        """Takes list of data frames and dictionary of replacement colNames and and renames specifies columns"""
        for df in dfs:
            df.rename(columns=colNames, inplace=True)

    def combineVertically(dfs):
        """Takes list of dataframes and returns a single dataframe of dfs stacked vertically"""
        stack = pd.concat(dfs, axis=0)
        stack['Date'] = pd.to_datetime(stack['Date'])
        return stack.sort_values('Date')

    def cleanedDailyAvg(dataFrame):
        """Takes a data frame. Averages variables by day"""
        temp = dataFrame
        temp.loc[temp['pH (total scale)']
                 == -999, ['pH (total scale)']] = np.nan
        day = temp.groupby('Date').mean()
        return day


#reading in data
ME_dfs = dataCleaning.folderToDfs('data/ME')
GA_dfs = dataCleaning.folderToDfs('data/GA')
FL_dfs = dataCleaning.folderToDfs('data/FL')

# Maine

# renaming mess variable names
ME_cols = {
    "pH_SW": "pH (total scale)",
    "pH_SW (Total Scale)": "pH (total scale)",
    "pH (total scale)": "pH (total scale)",
    'pH_QF': 'pH QF',
    'CHL': "CHL (ug/l)",
    'xCO2  Air (wet) (umol/mol)': 'xCO2 Air (wet) (umol/mol)',
    'xCO2  Air (wet) (umol/mol)': 'xCO2 Air (wet) (umol/mol)',
    'DOXY': 'DOXY (umol/kg)',
    'Licor Atm Pressure  (hPa)': 'Licor Atm Pressure (hPa)',
    'NTU': 'NTU (NTU)',
    'fCO2  Air (sat) uatm': 'fCO2 Air (sat) (uatm)',
    'fCO2  SW (sat) uatm': 'fCO2 SW (sat) (uatm)',
    'fCO2 Air (sat) uatm': 'fCO2 Air (sat) (uatm)',
    'pCO2 Air (sat) uatm': 'pCO2 Air (sat) (uatm)',
    'fCO2 SW (sat) uatm': 'fCO2 SW (sat) (uatm)',
    'fCO2  SW (sat) (uatm)': 'fCO2 SW (sat) (uatm)',
    'pCO2 SW (sat) uatm': 'pCO2 SW (sat) (uatm)',
    'xCO2  SW (dry) (umol/mol)': 'xCO2 SW (dry) (umol/mol)',
    'xCO2  SW (wet) (umol/mol)': 'xCO2 SW (wet) (umol/mol)',
    'xCO2  Air (dry) (umol/mol)': 'xCO2 Air (dry) (umol/mol)'

}
FL_cols = {
    "pH_SW": "pH (total scale)",
    "pH_SW (Total Scale)": "pH (total scale)",
    "pH (total scale)": "pH (total scale)",
    "pH SW": "pH (total scale)",
    "pH (total scale)": "pH (total scale)",
    'CHL': "CHL (ug/l)",
    'xCO2 Air (wet) (umol/mol)': 'xCO2 Air (wet) (umol/mol)',

    'Licor Atm Pressure  (hPa)': 'Licor Atm Pressure (hPa)',
    'fCO2  Air (sat) uatm': 'fCO2 Air (sat) (uatm)',
    'fCO2  SW (sat) uatm': 'fCO2 SW (sat) (uatm)',
    'pCO2 Air (sat) uatm': 'pCO2 Air (sat) (uatm)',
    'pCO2 SW (sat) uatm': 'pCO2 SW (sat) (uatm)',
    "% O2": "MAPCO2 %O2",
    'DOXY': 'DOXY (umol/kg)',
    'NTU': 'NTU (NTU)',

    'xCO2  Air (wet) (umol/mol)': 'xCO2 Air (wet) (umol/mol)',
    'xCO2  SW (dry) (umol/mol)': 'xCO2 SW (dry) (umol/mol)',
    'xCO2  Air (dry) (umol/mol)': 'xCO2 Air (dry) (umol/mol)',
    'xCO2  SW (wet) (umol/mol)': 'xCO2 SW (wet) (umol/mol)',
    'fCO2 Air (sat) uatm': 'fCO2 Air (sat) (uatm)',
    'fCO2 SW (sat) uatm': 'fCO2 SW (sat) (uatm)'



}


GA_cols = {
    "pH_SW": "pH (total scale)",
    "pH_SW (Total Scale)": "pH (total scale)",
    "pH (total scale)": "pH (total scale)",
    "pH SW": "pH (total scale)",
    "pH (total scale)": "pH (total scale)",
}

dataCleaning.renameCols(ME_dfs, ME_cols)
ME_DF = dataCleaning.combineVertically(ME_dfs)
ME_DF_AVG = dataCleaning.cleanedDailyAvg(ME_DF)


# Georgia

dataCleaning.renameCols(GA_dfs, GA_cols)
GA_DF = dataCleaning.combineVertically(GA_dfs)
GA_DF_AVG = dataCleaning.cleanedDailyAvg(GA_DF)


# Florida
dataCleaning.renameCols(FL_dfs, FL_cols)
FL_DF = dataCleaning.combineVertically(FL_dfs)
FL_DF_AVG = dataCleaning.cleanedDailyAvg(FL_DF)


# add site variable for single data frame
ME_DF_AVG['site'] = 'Gulf of Maine'
GA_DF_AVG['site'] = "Gray's Reef"
FL_DF_AVG['site'] = 'Cheeca Rocks'

# create one single data frame
all_df_avg = pd.concat([ME_DF_AVG, GA_DF_AVG, FL_DF_AVG], axis=0)


# all_df_avg = all_df_avg[all_df_avg['xCO2 Air (wet) (umol/mol)'] > 300]


# get list of variables for dropdown menu
variables = all_df_avg.columns.sort_values()
variables_2_use = ['site',
    'SST (C)', 'Salinity',

    'pCO2 Air (sat) (uatm)', 'pCO2 SW (sat) (uatm)',
    'pH (total scale)',
    'xCO2 Air (wet) (umol/mol)']

# variable_dict = [{'var': 'DOXY (umol/kg)', 'desc': }]
# get sites for site filter drop down
sites = all_df_avg['site'].unique()

#select varaibles to preserve
# all_df_avg = all_df_avg[]


##### filtering bad data

all_df_avg.loc[all_df_avg['DOXY (umol/kg)'] < 0, ['DOXY (umol/kg)']] = np.nan
all_df_avg.loc[all_df_avg['SST (C)'] < 0, ['SST (C)']] = np.nan
all_df_avg.loc[all_df_avg['Salinity'] < 0, ['Salinity']] = np.nan

# not sure what a good cutoff is for this
all_df_avg.loc[all_df_avg['dfCO2'] < -200, ['dfCO2']] = np.nan
all_df_avg.loc[all_df_avg['fCO2 Air (sat) (uatm)']
               < 300, ['fCO2 Air (sat) (uatm)']] = np.nan
all_df_avg.loc[all_df_avg['fCO2 SW (sat) (uatm)']
               < 0, ['fCO2 SW (sat) (uatm)']] = np.nan
all_df_avg.loc[all_df_avg['pCO2 Air (sat) (uatm)']
               < 300, ['pCO2 Air (sat) (uatm)']] = np.nan
all_df_avg.loc[all_df_avg['pCO2 SW (sat) (uatm)']
               < 0, ['pCO2 SW (sat) (uatm)']] = np.nan
all_df_avg.loc[all_df_avg['xCO2 Air (dry) (umol/mol)']
               < 300, ['xCO2 Air (dry) (umol/mol)']] = np.nan

all_df_avg.loc[all_df_avg['xCO2 Air (wet) (umol/mol)']
               < 300, ['xCO2 Air (wet) (umol/mol)']] = np.nan

all_df_avg.loc[all_df_avg['xCO2 SW (dry) (umol/mol)']
               < 0, ['xCO2 SW (dry) (umol/mol)']] = np.nan

all_df_avg.loc[all_df_avg['xCO2 SW (wet) (umol/mol)']
               < 0, ['xCO2 SW (wet) (umol/mol)']] = np.nan


### Creating map of study sites  #####
siteLocals = {
    'site': ['Gulf of Maine', "Gray's Reef",
             'Cheeca Rocks'],
    'Latitude': [43.0200, 31.4020, 24.8977],
    'Longitude': [-70.5400, - 80.8710, -80.6182]}
sCords = pd.DataFrame(siteLocals, columns=['site', 'Latitude', "Longitude"])

filtered_data = all_df_avg[variables_2_use]
filtered_data['year'] = filtered_data.index.year
filtered_data['month'] = filtered_data.index.month


#### CALCULATING COUNT OF OBSERVATIONS BY MONTH AND YEAR #########
ph_month_obs_count = filtered_data[filtered_data['pH (total scale)'].notnull()].groupby(
    ['site', 'month'], as_index=False).count()

ph_year_obs_count = filtered_data[filtered_data['pH (total scale)'].notnull()].groupby(
    ['site', 'year'], as_index=False).count()

ph_month_mean = filtered_data[filtered_data['pH (total scale)'].notnull()].groupby(
    ['site', 'month'], as_index=False).mean()



################ GRAPHS ################################

ph_sst = px.scatter(all_df_avg, y='pH (total scale)',
                 x='SST (C)', color='site', trendline="ols",
                 title="pH vs Sea Surface Temperature")
ph_sst.show()
ph_sst.write_image("./images/ph_sst.svg")



ph_time =px.scatter(all_df_avg, y='pH (total scale)',
                    color='site', trendline="ols",
                    title="pH over time")

ph_time.show()
ph_time.write_image('./images/ph_time.svg')


ph_pCO2 = px.scatter(filtered_data, x='pCO2 SW (sat) (uatm)', y='pH (total scale)',
                     color='site', trendline="ols",
                     title="pH vs partial pressure of CO2(aqueous)")

ph_pCO2.show()
ph_pCO2.write_image('./images/ph_pCO2.svg')



month_count = px.bar(ph_month_obs_count, x='month',
                     y='pH (total scale)', color='site',
                     title="Count of daily observations of pH by month",
                     labels={'pH (total scale)': 'Count of observations of pH (total scale)'}
                     )
month_count.show()
month_count.write_image('./images/month_count.svg')


year_count = px.bar(ph_year_obs_count, x='year',
                    y='pH (total scale)', color='site',
                    title="Count of daily observations of pH by year",
                    labels={'pH (total scale)': 'Count of observations of pH (total scale)'})
year_count.show()
year_count.write_image('./images/year_count.svg')

month_pH_box = px.box(filtered_data, x='month', y='pH (total scale)', color='site',
title='pH by month')

month_pH_box.show()
month_pH_box.write_image('./images/month_ph_box.svg')


month_pCO2_box = px.box(filtered_data, x='month',
                        y='pCO2 SW (sat) (uatm)', color='site',
                        title='pCO2 by month')
month_pCO2_box.show()
month_pCO2_box.write_image('./images/month_pCO2_box.svg')


year_pH_box = px.box(filtered_data[filtered_data['site']=='Gulf of Maine'], x='year',
                     y='pH (total scale)', color='site')
year_pH_box.show()

year_sst_box = px.box(filtered_data, x='year',
                     y='SST (C)', color='site',
                     title='Sea Surface Temperature by Month')
year_sst_box.show()
year_sst_box.write_image('./images/year_sst_box.svg')


year_pCO2_box = px.box(filtered_data, x='year',
                       y='pCO2 SW (sat) (uatm)', color='site',
                       title='pCO2 of sea water by year')
year_pCO2_box.show()
year_pCO2_box.write_image('./images/year_pCO2_box.svg')

pCO2_time = px.scatter(all_df_avg, y='pCO2 SW (sat) (uatm)',
                     color='site', trendline="ols",
                     title='pCO2 of sea water over time')

pCO2_time.show()
pCO2_time.write_image('./images/pCO2_time.svg')



# # def box_year_site():
# #     sites = ['Gulf of Maine',"Gray's Reef", "Cheeca Rocks"]
# #     for site in sites:
# #         year_pH_box = px.box(filtered_data[filtered_data['site'] == site], x='year',
# #                             y='pH (total scale)',  title=f'{site} pH Total Scale by year')
# #         year_pH_box.show()
# #         year_pH_box.writes_images(f'./images/{site}._year_pH_box.svg')


# # box_year_site()


# year_pH_box = px.box(filtered_data, x='year',
#                      y='pH (total scale)', color='site',
#                        title='pH (total scale) by year')
# year_pH_box.show()
# year_pH_box.write_image('./images/year_pH_box.svg')


site_pH_box = px.box(filtered_data, x='site',
                     y='pH (total scale)', color='site',
                       title='pH (total scale) by site')
site_pH_box.show()
site_pH_box.write_image('./images/site_pH_box.svg')

site_pco2_box = px.box(filtered_data, x='site',
                     y='pCO2 SW (sat) (uatm)', color='site',
                       title='pCO2 SW (sat) (uatm) by site')
site_pco2_box.show()
site_pco2_box.write_image('./images/site_pco2_box.svg')


site_sst_box = px.box(filtered_data, x='site',
                      y='SST (C)', color='site',
                      title='SST (C) by site')
site_sst_box.show()
site_sst_box.write_image('./images/site_sst_box.svg')
