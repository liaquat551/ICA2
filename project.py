import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go


education = pd.read_csv('https://raw.githubusercontent.com/liaquat551/programming-fundamentals/master/googleplaystore.csv')
education = education.fillna({'Rating': 0.0, 'Content Rating': 'Unrated'})

app = dash.Dash()

server = app.server

app.layout = html.Div(children=[
    dcc.Markdown('''
# Google playstore data
#### [Database link](https://raw.githubusercontent.com/liaquat551/programming-fundamentals/master/googleplaystore.csv)


---


This data contains 10842 Apps\n
Each app (row) has values for catergory, rating, size, and more.

'''),

    dcc.Dropdown(id= 'dropdown1',
                 options=[
                     {'label': 'Apps by content rating', 'value':'pie'},
                     {'label': 'App installs by type', 'value':'histogram'},
                     {'label': 'App rating by type', 'value':'box'},],
                     value = 'histogram'
                ),
    dcc.Graph(id='graph')
])
@app.callback(Output('graph', 'figure'),[Input('dropdown1', 'value')])
def update_output_div(graph_type):
    if graph_type == 'pie':
        values = []
        for contenttype in education['Content Rating'].unique():
            count = education[(education['Content Rating'] == contenttype)]['Content Rating'].count()
            values.append(count)
        fig = {
  "data": [
    {
      "values": values,
      "labels": education['Content Rating'].unique(),
      "hoverinfo":"label+percent",
      "type": "pie"
    }],
    "layout": {
        "title":"Apps by content rating",
    }}
    elif graph_type == 'box':
        trace1 = go.Box(
            y = education.loc[(education.Type == 'Free')].Rating,
            name = 'Free',
        )

        trace2 = go.Box(
            y = education.loc[(education.Type == 'Paid')].Rating,
            name = 'Paid',
        )

        layout = go.Layout(
        title = 'App rating by type',
        showlegend = True,
        xaxis=dict(
        title="App type"),
        )

        data = [trace1, trace2,]
        fig = dict(data=data, layout=layout)
    else:
        trace1 = go.Histogram(
        x=education[education.Type == 'Paid'].Installs,
        name = 'Ratings of paid games'
            )
        trace2 = go.Histogram(
        x=education[education.Type == 'Free'].Installs,
        name = 'Ratings of free games'
        )
        data = [trace1, trace2]
        layout = go.Layout(
        title = 'App installs by type'
        )
        fig = dict(data=data, layout=layout)
    
    return fig
        
        
        
if __name__=='__main__':
    app.run_server(debug= True)