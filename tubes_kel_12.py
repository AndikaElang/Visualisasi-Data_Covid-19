# -*- coding: utf-8 -*-
"""TUBES_KEL_12.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iQtJNGLp7qHv8r_IEWGJMurupCVemWU6

## Maulidan Aziz - 1301183472
## Vianka Tetiana - 1301184138 
## Indira Alima Fasyazahra - 1301184051
"""

import numpy as np
import pandas as pd
from bokeh.plotting import figure, show
from bokeh.io import output_notebook, output_file
from bokeh.models import ColumnDataSource, HoverTool, CheckboxGroup, CustomJS, Panel, Tabs, Slider
from bokeh.transform import dodge
from bokeh.layouts import row
from bokeh.plotting import Figure
from bokeh.layouts import column
from bokeh.palettes import Viridis3

#Read Data
df_provinsi = pd.read_csv('https://raw.githubusercontent.com/AndikaElang/tubes-visdat/main/data_provinsi.csv?token=GHSAT0AAAAAABQWQJ3RTF5IDSF6DUUKBERCYPK53CQ')
df_provinsi

#Dictionary
data = {'provinsi'    : df_provinsi['Provinsi_Asal'].tolist(),
        'Kasus'       : df_provinsi['Kasus'].tolist(),
        'Sembuh'      : df_provinsi['Sembuh'].tolist(),
        'Meninggal'   : df_provinsi['Meninggal'].tolist()}

source = ColumnDataSource(data=data)

#menampilkan bokeh 
output_notebook()

#menyimpan hasil boleh
output_file('covid.html', title='Data Covid 19')

"""## 1. Visualisasi data covid berdasarkan negara Indonesia"""

#Untuk Bar kasus, sembuh, dan meninggal
p = figure(x_range=df_provinsi['Provinsi_Asal'], y_range=(0, 1000), plot_height=500, plot_width=2000, title="Data Persebaran Virus COVID-19 di Indonesia", toolbar_location="left")

p.vbar(x=dodge('provinsi', -0.25, range=p.x_range), top='Kasus', width=0.2, source=source,
       color="navy", legend_label="Kasus")

p.vbar(x=dodge('provinsi',  0.0,  range=p.x_range), top='Sembuh', width=0.2, source=source,
       color="green", legend_label="Sembuh")

p.vbar(x=dodge('provinsi',  0.25, range=p.x_range), top='Meninggal', width=0.2, source=source,
       color="gray", legend_label="Meninggal")


p.x_range.range_padding = 0.01
p.xgrid.grid_line_color = None
p.legend.location = "top_left"
p.legend.orientation = "horizontal"

# Font
p.xaxis.major_label_text_font_size = '6pt'
p.yaxis.major_label_text_font_size = '10pt'

#Hover untuk melihat data lebih detail
hover = HoverTool()
hover.tooltips = [
    ("Jumlah Kasus", "@Kasus Pasien"),
    ("Jumlah Sembuh", "@Sembuh Pasien"),
    ("Jumlah Meninggal", "@Meninggal Pasien")]

hover.mode = 'vline'

p.add_tools(hover)

#Output 
show(p)

"""## 2. Visualisasi data covid berdasarkan Pulau di Indonesia"""

#Read dataset berdasarkan provinsi di pulau jawa
df_jawa = df_provinsi.iloc[[0, 1, 2, 3, 5, 17], :]

#Setup figur untuk kasus, sembuh, meninggal. 
fig1 =figure(title="Data Kasus Positif COVID-19 di Jawa", x_range=df_jawa['Provinsi_Asal'].tolist(), plot_width=800, plot_height=300)
fig1.vbar(x=df_jawa['Provinsi_Asal'].tolist(), top=df_jawa['Kasus'].tolist(), width=0.8, color='gray')
tab1 = Panel(child=fig1, title="Kasus")

fig2 =figure(title="Data Pasien Sembuh dari COVID-19 di Jawa", x_range=df_jawa['Provinsi_Asal'].tolist(), plot_width=800, plot_height=300)
fig2.vbar(x=df_jawa['Provinsi_Asal'].tolist(), top=df_jawa['Sembuh'].tolist(), width=0.8, color='aqua')
tab2 = Panel(child=fig2, title="Sembuh")

fig3 =figure(title="Data Kematian akibat COVID-19 di Sumatera", x_range=df_jawa['Provinsi_Asal'].tolist(), plot_width=800, plot_height=300)
fig3.vbar(x=df_jawa['Provinsi_Asal'].tolist(), top=df_jawa['Meninggal'].tolist(), width=0.8, color='red')
tab3 = Panel(child=fig3, title="Meninggal")

def set_style(p):
# Tick labels
    p.xaxis.major_label_text_font_size = '6pt'
    p.yaxis.major_label_text_font_size = '10pt'


#Set Tab Kasus, Sembuh, Meninggal
tabs = Tabs(tabs=[ tab1, tab2, tab3])

set_style(fig1)
set_style(fig2)
set_style(fig3)

#Output
show(tabs)

