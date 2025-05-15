import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

mouse_data = pd.read_csv('Mouse_metadata.csv')
study_results = pd.read_csv('Study_results.csv')
merged_df = pd.merge(mouse_data, study_results, on = 'Mouse ID')

# --------------------------------------------------------------------------------------
#											PART 1: DESIGN PARAMETERS
# --------------------------------------------------------------------------------------
# Here we will set the colors, margins, DIV height&weight and other parameters
color_choices = {
	'light-blue': '#7FAB8',
	'light-grey': '#F7EFED',
	'light-red':  '#F1485B',
	'dark-blue':  '#33546D',
	'middle-blue': '#61D4E2'
}

drug_colors = {
	'Placebo':		'#29304E',
	'Capomulin':	'#27706B',	
	'Ramicane':		'#71AB7F',
	'Ceftamin':		'#9F4440',
	'Infubinol':	'#FFD37B',
	'Ketapril':		'#FEADB9',
	'Naftisol':		'#B3AB9E',
	'Propriva':		'#ED5CD4',
	'Stelasyn':		'#97C1DF',
	'Zoniferol':	'#8980D4'
}

colors = {
		'full-background':		color_choices['light-grey'],
		'chart-background':		color_choices['light-grey'],
		'histogram-color-1':	color_choices['dark-blue'],
		'histogram-color-2':	color_choices['light-red'],
		'block-borders':		color_choices['dark-blue']
}

margins = {
		'block-margins': '10px 10px 10px 10px',
		'block-margins': '4px 4px 4px 4px'
}

sizes = {
		'subblock-heights': '290px'
}
# ------------------------------------------------------------------------------------------
#											PART 2: ACTUAL LAYOUT
# ------------------------------------------------------------------------------------------
# Here we will set the DIV-s and other parts of our layout
# We need to have a 2x2 grid
# I have also included 1 more grid on top of others, where we will show the title of the app
# DIV for TITLE
div_title = html.Div(children =	html.H1('Title'),
					style ={
							'border': '3px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'text-align': 'center'
							}
					)

# DIV for first row (1.1 and 1.2)
# inside DIV 1.1
div_1_1_button = dcc.Checklist(
				id = 'weight-histogram-checklist',
		        options=[
		        	{'label': drug, 'value': drug}
					for drug in np.unique(mouse_data['Drug Regimen'])
		        ],
		        value=['Placebo'],
		        labelStyle={'display': 'inline-block'}
			)

div_1_1_graph = dcc.Graph(
				id = 'weight-histogram',
			)

div_1_1 = html.Div(children=[div_1_1_button, div_1_1_graph],
    style={
        'border': '1px {} solid'.format(colors['block-borders']),
        'margin': margins['block-margins'],
        'width': '48%',
        'padding': '10px',
        'box-sizing': 'border-box',
        'overflow': 'hidden'
    }
)
# --------------------------------------------------------------------------------------
# inside DIV 2.1
div_2_1_button = dcc.RadioItems(
				id = 'weight-histogram-radioItems',
		        options=[
		        	{'label': drug, 'value': drug}
					for drug in np.unique(mouse_data['Drug Regimen'])
		        ],
		        value='Placebo',
		        labelStyle={'display': 'inline-block'}
			)

div_2_1_graph = dcc.Graph(
				id = 'weight-histogram_2',
				figure = {}
			)

div_2_1 = html.Div(children=[div_2_1_button, div_2_1_graph],
    style={
        'border': '1px {} solid'.format(colors['block-borders']),
        'margin': margins['block-margins'],
        'width': '48%',
        'padding': '10px',
        'box-sizing': 'border-box',
        'overflow': 'hidden'
    }
)
# Collecting all DIV-s in the final layout
# Here we collect all DIV-s into a final layout DIV
app.layout = html.Div(	[
						div_title,
						div_1_1,
						div_2_1
						],
						style = {
							'backgroundColor': colors['full-background']
						}
					)
# -------------------------------------------------------------------------------------
# histogram of mice weights' for each drug
# it is a stacked histogram which lets us put histograms on top of each other 
@app.callback(
    Output(component_id='weight-histogram', component_property='figure'),
    [Input(component_id='weight-histogram-checklist', component_property='value')]
)
def update_weight_histogram(drug_names):
    traces = []

    for drug in drug_names:
        traces.append(go.Histogram(
            x=mouse_data[mouse_data['Drug Regimen'] == drug]['Weight (g)'],
            name=drug,
            opacity=0.7,
            marker=dict(color=drug_colors[drug])
        ))

    return {
        'data': traces,
        'layout': dict(
            barmode='stack',
            yaxis=dict(title='number of mice'),
            xaxis=dict(title='mouse weight'),
            autosize=True,
            paper_bgcolor=colors['chart-background'],
            plot_bgcolor=colors['chart-background'],
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            height=400
        )
    }
# -------------------------------------------------------------------------------------
@app.callback(
    Output(component_id='weight-histogram_2', component_property='figure'),
    [Input(component_id='weight-histogram-radioItems', component_property='value')]
)
def update_weight_histogram_2(drug_name):
    traces = []
    traces.append(go.Histogram(
        x=mouse_data[mouse_data['Drug Regimen'] == drug_name]['Weight (g)'],
        name=drug_name,
        opacity=0.7,
        marker=dict(color=drug_colors[drug_name])
    ))
    traces.append(go.Histogram(
        x=mouse_data['Weight (g)'],
        name="all mice",
        opacity=0.7,
        marker=dict(color='#8980D4')
    ))
    return {
        'data': traces,
        'layout': dict(
            barmode='stack',
            yaxis=dict(title='number of mice'),
            xaxis=dict(title='mouse weight'),
            autosize=True,
            paper_bgcolor=colors['chart-background'],
            plot_bgcolor=colors['chart-background'],
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            height=400
        )
    }
# ----------------------------------------------------------------------------------------
#											PART 3:
# ----------------------------------------------------------------------------------------
drug_groups = {
    'Lightweight': ['Ramicane', 'Capomulin'],
    'Heavyweight': ['Infubinol', 'Ceftamin'],
    'Placebo': ['Placebo']
}

div_group_selector = dcc.RadioItems(
    id='drug-group-selector',
    options=[{'label': k, 'value': k} for k in drug_groups],
    value='Placebo',
    labelStyle={'display': 'inline-block'}
)

div_3 = html.Div(children=[
    div_group_selector,
    dcc.Graph(id='chart-3-weight-survival')
], style={
    'border': '1px {} solid'.format(colors['block-borders']),
    'margin': margins['block-margins'],
    'width': '48%',
    'height': '500px',
    'padding': '10px',
    'box-sizing': 'border-box'
})

# ------------------------------------------------------------------------------------------
@app.callback(
    Output('chart-3-weight-survival', 'figure'),
    [Input('drug-group-selector', 'value')]
)
def update_chart3(group):
    traces = []
    for drug in drug_groups[group]:
        weights = merged_df[merged_df['Drug Regimen'] == drug]['Weight (g)']
        traces.append(go.Histogram(
            x=weights,
            name=drug,
            opacity=0.7,
            marker=dict(color=drug_colors.get(drug, '#333'))
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            barmode='stack',
            yaxis=dict(title='number of mice'),
            xaxis=dict(title='mouse weight'),
            paper_bgcolor=colors['chart-background'],
            plot_bgcolor=colors['chart-background'],
            margin=dict(l=40, b=40, t=10, r=10),
            legend=dict(x=0, y=1),
            height=400
        )
    }
# ------------------------------------------------------------------------------------------
#											PART 4:
# ------------------------------------------------------------------------------------------
div_4 = html.Div(children=[
    dcc.Graph(id='chart-4-time-survival')
], style={
    'border': '1px {} solid'.format(colors['block-borders']),
    'margin': margins['block-margins'],
    'width': '48%',
    'height': '500px',
    'padding': '10px',
    'box-sizing': 'border-box'
})
# -------------------------------------------------------------------------------------------
@app.callback(
    Output('chart-4-time-survival', 'figure'),
    [Input('drug-group-selector', 'value')]
)
def update_chart4(group):
    traces = []

    for drug in drug_groups[group]:
        group_df = merged_df[merged_df['Drug Regimen'] == drug]
        survival_counts = group_df.groupby('Timepoint')['Mouse ID'].nunique().sort_index(ascending=True)
        survival = survival_counts[::-1].cumsum()[::-1]

        traces.append(go.Scatter(
            x=survival.index,
            y=survival.values,
            mode='lines+markers',
            name=drug,
            marker=dict(color=drug_colors.get(drug, '#333'))
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            yaxis=dict(title='number of alive mice'),
            xaxis=dict(title='time point'),
            paper_bgcolor=colors['chart-background'],
            plot_bgcolor=colors['chart-background'],
            margin=dict(l=40, b=40, t=10, r=10),
            legend=dict(x=0, y=1),
            height=400
        )
    }
# ------------------------------------------------------------------------------------------
row_1 = html.Div([div_1_1, div_2_1], style={
    'display': 'flex',
    'justify-content': 'space-between'
})

row_2 = html.Div([div_3, div_4], style={
    'display': 'flex',
    'justify-content': 'space-between'
})

app.layout = html.Div([
    div_title,
    row_1,
    row_2
], style={
    'backgroundColor': colors['full-background'],
    'padding': '20px'
})

# >> use __ debug=True __ in order to be able to see the changes after refreshing the browser tab,
#			 don't forget to save this file before refreshing
# >> use __ port = 8081 __ or other number to be able to run several apps simultaneously
if __name__ == '__main__':
	app.run(debug=True, 
	port = 8081)