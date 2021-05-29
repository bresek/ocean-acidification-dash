
# Talked with Prof. Magee and we did not see a purpose in having an __init__ or __repr__ method at the present. She told me to write this here
#! Run this app with `python app.py` in your terminal and
#! visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import os
import matplotlib
import numpy as np



# defining data processing functions
class dataCleaning:
    def folderToDfs(folderpath):
        """returns list of dataframes from an input folder"""
        files = os.listdir(folderpath)
        df_list = []
        for file in files:
            if not file.startswith('.'):
                print(file)
                temp_df = pd.read_csv(folderpath+'/'+file)
                df_list.append(temp_df)
        return df_list

    def renameCols(dfs, colNames):
        """Takes list of data frames and dictionary of replacement colNames and and renames specifies columns"""
        for df in dfs:
            df.rename(columns=colNames, inplace=True)

    #     print(df.columns)
    def combineVertically(dfs):
        """Takes list of dataframes and returns a single dataframe of dfs stacked vertically"""
        stack = pd.concat(dfs, axis=0)
        stack['Date'] = pd.to_datetime(stack['Date'])
        return stack.sort_values('Date')

    def cleanedDailyAvg(dataFrame):
        """Takes a data frame. Averages variables by day"""
        # temp = dataFrame[dataFrame['pH_total_scale'] != -999]
        temp = dataFrame
        temp.loc[temp['pH_total_scale']
                 == -999, ['pH_total_scale']] = np.nan
        
        # temp['Month'] = pd.DatetimeIndex(temp['Date']).month
        # temp['Year'] = pd.DatetimeIndex(temp['Date']).year
        # day = temp.resample('Y').mean()
        # monthly = day.groupby(['Month'], ['Year']).mean()
        day = temp.groupby('Date').mean()
      
        return  day


#reading in data
ME_dfs = dataCleaning.folderToDfs('analysis/data/ME')
GA_dfs = dataCleaning.folderToDfs('analysis/data/GA')
FL_dfs = dataCleaning.folderToDfs('analysis/data/FL')

# Maine


ME_cols =  {
    "pH_SW": "pH_total_scale",
    "pH_SW (Total Scale)": "pH_total_scale",
    "pH (total scale)": "pH_total_scale",
    'pH_QF' : 'pH QF',
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
    "pH_SW": "pH_total_scale",
    "pH_SW (Total Scale)": "pH_total_scale",
    "pH (total scale)": "pH_total_scale",
    "pH SW": "pH_total_scale",
    "pH_Total_Scale": "pH_total_scale",
        'CHL': "CHL (ug/l)",
        'xCO2 Air (wet) (umol/mol)': 'xCO2 Air (wet) (umol/mol)',

        'Licor Atm Pressure  (hPa)': 'Licor Atm Pressure (hPa)',
        'fCO2  Air (sat) uatm': 'fCO2 Air (sat) (uatm)',
        'fCO2  SW (sat) uatm': 'fCO2 SW (sat) (uatm)',
        # 'fCO2 Air (sat) uatm': 'fCO2 Air (sat) (uatm)',
        'pCO2 Air (sat) uatm': 'pCO2 Air (sat) (uatm)',
        # 'fCO2 SW (sat) uatm': 'fCO2 SW (sat) (uatm)',
        # 'fCO2  SW (sat) (uatm)': 'fCO2 SW (sat) (uatm)',
        'pCO2 SW (sat) uatm': 'pCO2 SW (sat) (uatm)',
        "% O2": "MAPCO2 %O2",
        'DOXY': 'DOXY (umol/kg)',
        'NTU' : 'NTU (NTU)',
        
        'xCO2  Air (wet) (umol/mol)': 'xCO2 Air (wet) (umol/mol)',
        'xCO2  SW (dry) (umol/mol)': 'xCO2 SW (dry) (umol/mol)',
        'xCO2  Air (dry) (umol/mol)': 'xCO2 Air (dry) (umol/mol)',
        'xCO2  SW (wet) (umol/mol)': 'xCO2 SW (wet) (umol/mol)',
        'fCO2 Air (sat) uatm' : 'fCO2 Air (sat) (uatm)',
        'fCO2 SW (sat) uatm' : 'fCO2 SW (sat) (uatm)'



}


GA_cols = {
    "pH_SW": "pH_total_scale",
    "pH_SW (Total Scale)": "pH_total_scale",
    "pH (total scale)": "pH_total_scale",
    "pH SW": "pH_total_scale",
    "pH_Total_Scale": "pH_total_scale",
    # 'fCO2 Air (sat) uatm': 'fCO2 Air (sat) (uatm)'

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
ME_DF_AVG['site'] = 'ME'
GA_DF_AVG['site'] = 'GA'
FL_DF_AVG['site'] = 'FL'

# create one single data frame
all_df_avg = pd.concat([ME_DF_AVG, GA_DF_AVG, FL_DF_AVG], axis=0)


# all_df_avg = all_df_avg[all_df_avg['xCO2 Air (wet) (umol/mol)'] > 300]

#select varaibles to preserve
# all_df_avg = all_df_avg[]

# all_df_avg = all_df_avg[all_df_avg['CO2 SW QF'] == 2]

# get list of variables for dropdown menu                         
variables = all_df_avg.columns.sort_values()
variables_2_use = [ 
                   'SST (C)', 'Salinity',
                   
                   'pCO2 Air (sat) (uatm)', 'pCO2 SW (sat) (uatm)',
                   'pH_total_scale', 
                   'xCO2 Air (wet) (umol/mol)']

# variable_dict = [{'var': 'DOXY (umol/kg)', 'desc': }]
# get sites for site filter drop down
sites = all_df_avg['site'].unique()
sites
print(variables.sort_values())

# all_df_avg[all_df_avg[]]
# temp = dataFrame[dataFrame['SST (C)'] > 0]

##### filtering bad data???
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



################################# dash app #######################

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

# print(ME_DF_AVG['site'])

graph_me = px.scatter(all_df_avg, y="pH_total_scale",
                      trendline="ols", color='site')
graph_2 = px.scatter(all_df_avg[all_df_avg['SST (C)'] > 0], y="pH_total_scale", x="SST (C)",
                     trendline="ols", color='site')
graph_fl = px.scatter(FL_DF_AVG, y="pH_total_scale", trendline="ols")


# 3 input parameters I think (1) Y variable (2) x variable (3)site (4??) avg by day, month, year?

# Getting date to be apart of the xvariables
xVariables = [{'label': i, 'value': i}
     for i in variables_2_use]
dateLabel = {'label': "Date", 'value': ''}
xVariables.append(dateLabel)


app.layout = html.Div(children=[

    html.H1(children='Ocean Acidification'),
    html.P(children=f"Number of varibles: {len(variables_2_use)}. DataFrame dimensions: {all_df_avg.shape}"),

    html.Div(id = "interactive plot",children =[ 
        dcc.Dropdown(
                id='xaxis',
            options=xVariables,
                value=''
                ),
        dcc.Dropdown(
            id='yaxis',
            options=[{'label': i, 'value': i} for i in variables_2_use],
            value="pH_total_scale"
        ),
        
        dcc.Dropdown(
            id='site_selector',
            options=[{'label': i, 'value': i} for i in sites],
            
            value=sites,
            multi=True


        ),
        dcc.RadioItems(
            id='avgRange',
            options=[
                {'label': 'Daily', 'value': 'D'},
                {'label': 'Weekly', 'value': 'W'},
                {'label': 'Monthly', 'value': 'M'},
                {'label': 'Yearly', 'value': 'Y'},
            ],
            value= 'Y'
        ),
        dcc.Graph(id='indicator-graphic'),
   ]),
   html.Div(id='citation',
            children="Data from Sutton, A. J., Feely, R. A., Maenner-Jones, S., Musielwicz, S., Osborne, J., Dietrich, C., Monacci, N., Cross, J., Bott, R., Kozyr, A., Andersson, A. J., Bates, N. R., Cai, W.-J., Cronin, M. F., De Carlo, E. H., Hales, B., Howden, S. D., Lee, C. M., Manzello, D. P., McPhaden, M. J., Meléndez, M., Mickett, J. B., Newton, J. A., Noakes, S. E., Noh, J. H., Olafsdottir, S. R., Salisbury, J. E., Send, U., Trull, T. W., Vandemark, D. C., and Weller, R. A. (2019): Autonomous seawater pCO2 and pH time series from 40 surface buoys and the emergence of anthropogenic trends, Earth Syst. Sci. Data, 11, 421-439, https://doi.org/10.5194/essd-11-421-2019.")

])


@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('xaxis', 'value'),
    Input('yaxis', 'value'),
    Input('site_selector', "value"),
    Input('avgRange', 'value')
)
def update_graph(xaxis, yaxis, site_selector, avgRange):
    
   


    print(f"site_selector {site_selector}")
    print(type(site_selector))

    if type(site_selector) == list:
        data = all_df_avg[all_df_avg.site.isin(
            site_selector)]
    else:
        data = all_df_avg[all_df_avg['site'] == site_selector]

   
    

    if xaxis == '':
        fig = px.scatter(data, y=data[yaxis], trendline="ols", color='site')
    else:
        fig = px.scatter(data , x=data[xaxis],
                         y=data[yaxis], trendline="ols", color='site')



    fig.update_xaxes(rangeslider_visible=True)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
