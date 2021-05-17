
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import os
import matplotlib



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

    #     print(df.columns)
    def combineVertically(dfs):
        """Takes list of dataframes and returns a single dataframe of dfs stacked vertically"""
        stack = pd.concat(dfs, axis=0)
        stack['Date'] = pd.to_datetime(stack['Date'])
        return stack.sort_values('Date')

    def cleanedDailyAvg(dataFrame):
        """Takes a data frame. Averages variables by day"""
        temp = dataFrame[dataFrame['pH_total_scale'] > 0]
        return temp.groupby(['Date']).mean()


#reading in data
ME_dfs = dataCleaning.folderToDfs('analysis/data/ME')
GA_dfs = dataCleaning.folderToDfs('analysis/data/GA')
FL_dfs = dataCleaning.folderToDfs('analysis/data/FL')

## Maine

columns = {
    "pH_SW": "pH_total_scale",
    "pH_SW (Total Scale)": "pH_total_scale",
    "pH (total scale)": "pH_total_scale",
    "pH SW": "pH_total_scale",
    "pH_Total_Scale": "pH_total_scale"
}
dataCleaning.renameCols(ME_dfs, columns)
ME_DF = dataCleaning.combineVertically(ME_dfs)
ME_DF_AVG = dataCleaning.cleanedDailyAvg(ME_DF)


## Georgia

dataCleaning.renameCols(GA_dfs, columns)
GA_DF = dataCleaning.combineVertically(GA_dfs)
GA_DF_AVG = dataCleaning.cleanedDailyAvg(GA_DF)


## Florida
dataCleaning.renameCols(FL_dfs, columns)
FL_DF = dataCleaning.combineVertically(FL_dfs)
FL_DF_AVG = dataCleaning.cleanedDailyAvg(FL_DF)


# combine into one 
ME_DF_AVG['site'] = 'ME'
GA_DF_AVG['site'] = 'GA'
FL_DF_AVG['site'] = 'FL'

all_df_avg = pd.concat([ME_DF_AVG, GA_DF_AVG, FL_DF_AVG], axis=0)
# all_df_avg[all_df_avg[]]
# temp = dataFrame[dataFrame['SST (C)'] > 0]


################################# dash app #######################

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

# print(ME_DF_AVG['site'])

graph_me = px.scatter(all_df_avg, y="pH_total_scale", trendline="ols", color='site')
graph_2 = px.scatter(all_df_avg[all_df_avg['SST (C)'] > 0], y="pH_total_scale", x="SST (C)",
                     trendline="ols", color='site')
graph_fl = px.scatter(FL_DF_AVG, y="pH_total_scale", trendline="ols")


#3 input parameters I think (1) Y variable (2) x variable (3)site (4??) avg by day, month, year?


app.layout = html.Div(children=[
    html.H1(children='Ocean Acidification'),

    html.Div(children='''
        Maine, Georgia, Florida
    '''),
    dcc.Graph(
        id='me ph graph',
        figure=graph_me
    ),
    dcc.Graph(
        id="ga ph graph",
        figure=graph_2
    ),
    dcc.Graph(
        id='fl ph graph',
        figure=graph_fl
    ),




])

if __name__ == '__main__':
    app.run_server(debug=True)
