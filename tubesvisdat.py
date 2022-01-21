# -*- coding: utf-8 -*-
"""TubesVisdat.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TO-zYVo5z4j7G2M8jrftSmasmtIeYf_u
"""

import pandas as pd
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import CategoricalColorMapper
from bokeh.palettes import Spectral6
from bokeh.layouts import widgetbox, row, gridplot
from bokeh.models import Slider, Select

data = pd.read_csv("https://raw.githubusercontent.com/MRifqiWiliatama/tubes-visdat/main/datacovmar.csv")
data.set_index('Date', inplace=True)
data

data = data.drop(labels=['Location ISO Code', 'Total Active Cases', 'Location Level', 'City or Regency',
                  'Country', 'Continent', 'Island', 'Time Zone', 'Special Status', 'Total Regencies', 'Total Cities',
                  'Total Districts', 'Total Urban Villages', 'Total Rural Villages', 'Area (km2)', 'Population',
                  'Population Density', 'Longitude', 'Latitude', 'New Cases per Million', 'Total Cases per Million',
                  'New Deaths per Million', 'Total Deaths per Million', 'Total Deaths per 100rb', 'Case Fatality Rate',
                  'Case Recovered Rate', 'Growth Factor of New Cases', 'Growth Factor of New Deaths'], axis=1)
data.head()

data = data.dropna()
data.head()

data = data.rename(columns={"Location": "location", "New Cases": "new_cases", "New Deaths": "new_deaths", "New Recovered": "new_recovered", 
                            "New Active Cases": "new_active_cases", "Total Cases": "total_cases", "Total Deaths": "total_deaths", "Total Recovered": "total_recovered", 
                            "Province": "province"})
data.head()

# Make a list of the unique values from the province column: province_list
province_list = data.province.unique().tolist()

# Make a color mapper: color_mapper
color_mapper = CategoricalColorMapper(factors=province_list, palette=Spectral6)

# Make the ColumnDataSource: source
source = ColumnDataSource(data={
    'x'          : data.loc[2].total_cases,
    'y'          : data.loc[2].total_deaths,
    'location'   : data.loc[2].location,
    'province'   : data.loc[2].province,
})

# Create the figure: plot
plot = figure(title='1970', x_axis_label='Total Cases', y_axis_label='Total Deaths',
           plot_height=400, plot_width=700, tools=[HoverTool(tooltips='@location')])

# Add a circle glyph to the figure p
plot.circle(x='x', y='y', source=source, fill_alpha=0.8,
           color=dict(field='province', transform=color_mapper), legend='province')

# Set the legend and axis attributes
plot.legend.location = 'bottom_left'

# Define the callback function: update_plot
def update_plot(attr, old, new):
    # set the `yr` name to `slider.value` and `source.data = new_data`
    date = slider.value
    x = x_select.value
    y = y_select.value
    # Label axes of plot
    plot.xaxis.axis_label = x
    plot.yaxis.axis_label = y
    # new data
    new_data = {
    'x'          : data.loc[date][x],
    'y'          : data.loc[date][y],
    'location'   : data.loc[date].location,
    'province'   : data.loc[date].province,
    }
    source.data = new_data
    
    # Add title to figure: plot.title.text
    plot.title.text = 'COVID-19 Statistic for March %d' % date

# Make a slider object: slider
slider = Slider(start=1, end=31, step=1, value=1, title='Date')
slider.on_change('value',update_plot)

# Make dropdown menu for x and y axis
# Create a dropdown Select widget for the x data: x_select
x_select = Select(
    options=['new_cases', 'new_deaths', 'new_recovered', 'new_active_cases', 'total_cases', 'total_deaths', 'total_recovered'],
    value='total_cases',
    title='x-axis data'
)
# Attach the update_plot callback to the 'value' property of x_select
x_select.on_change('value', update_plot)

# Create a dropdown Select widget for the y data: y_select
y_select = Select(
    options=['new_cases', 'new_deaths', 'new_recovered', 'new_active_cases', 'total_cases', 'total_deaths', 'total_recovered'],
    value='total_deaths',
    title='y-axis data'
)
# Attach the update_plot callback to the 'value' property of y_select
y_select.on_change('value', update_plot)
    
# Create layout and add to current document
layout = row(widgetbox(slider, x_select, y_select), plot)
curdoc().add_root(layout)

# bokeh serve -- show TubesVisdat.py

# !pip freeze > requirements.txt

curdoc().clear()