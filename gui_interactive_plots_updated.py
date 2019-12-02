import streamlit as st
import json
import pandas as pd
import numpy as np
from numpy import linspace, meshgrid
import matplotlib.pylab as plt
from plotly.offline import download_plotlyjs, plot
from plotly.graph_objs import Scatter, Layout, Contour, Heatmap, Surface, Scatter3d
import plotly.graph_objects as go
from inference.gp_tools import GpRegressor

st.title('Simple TBR plotter')

@st.cache
def load_data():
    return pd.read_json('results.json') 

data = load_data()

# st.write(data[0])

st.write(data.keys())
firstwall_coolant = st.selectbox('select a firstwall coolant', data['firstwall_coolant'].unique())
blanket_multiplier_material = st.selectbox('select a blanket multiplier material', data['blanket_multiplier_material'].unique())
blanket_breeder_material = st.selectbox('select a blanket breeder material', data['blanket_breeder_material'].unique())

blanket_steel_fraction = st.slider('Select a range of blanket steel fractions', min_value=0.0, max_value=1.0, value=0.1, step=0.1)

filtered_data = data[
                     (data.firstwall_coolant == firstwall_coolant) & 
                     (data.blanket_multiplier_material == blanket_multiplier_material) &
                     (data.blanket_breeder_material == blanket_breeder_material) &
                     (data.blanket_steel_fraction >= blanket_steel_fraction-0.001) & (data.blanket_steel_fraction <= blanket_steel_fraction+0.001)
                    ]

def make_2d_surface_trace(gp_mu_folded,x_gp,y_gp,z_axis_title):
        trace = Contour(
            z=gp_mu_folded,
            x=x_gp,
            y=y_gp,
            colorscale='Viridis',
            colorbar={'title':z_axis_title,
                      'titleside':'right',
                      'titlefont':dict(size=15),
                      'tickfont':dict(size=15)},
            opacity=0.9,
            line= dict(width=1,smoothing=0.85),
            contours=dict(
                # showlines=False,
                # showlabels=False,
                coloring= "heatmap",
                start=min(gp_mu),
                end=max(gp_mu),
                size=0.05,
                        labelfont=dict(
                            size=15,
                        ),
                )
        )
        return trace

def make_2d_scatter_trace(x,y,z,text_values, name=''):
        trace = Scatter(x=x, 
                        y=y,
                        mode = 'markers',
                        name = name,
                        hoverinfo='text' ,
                        text=text_values,
                        marker = {'size':6,
                                       'color':'red',
                                       'symbol':'cross'} 
        )
        return trace

def generate_2d_layout(title,x_axis_name,y_axis_name,x,y):
    layout = Layout(xaxis={'title':x_axis_name, 
                           'showline':True,
                           'range':[min(x),max(x)],
                           'mirror':"ticks",
                           'ticks':"outside",
                           "linewidth":3,
                           "tickwidth":3,
                           'titlefont':dict(size=20),
                            'tickfont':dict(size=15)                       
                           },
                    yaxis={'title':y_axis_name,
                           'showline':True,
                           'range':[min(y),max(y)],
                           'mirror':"ticks",
                           'ticks':"outside",
                           "linewidth":3,
                           "tickwidth":3,
                           'titlefont':dict(
                                size=20,
                            ),
                            'tickfont':dict(
                                size=15,
                            )
                          },
                    margin=dict(l=80, r=10, b=80, t=50),
                    hovermode = 'closest',
                    title=title,
                    titlefont=dict(size=20)   ,                 
                    legend={'y': 0.7,#.1,
                             'x': 0.1,
                             #'orientation': "h",
                              'font':dict(size=10),
                            },
                    )
    return layout

# try:
x = list(filtered_data.blanket_breeder_li6_enrichment_fraction)
y = list(filtered_data.fraction_of_breeder_in_breeder_plus_multiplier_volume)
z = list(filtered_data.tbr)
z_e = list(filtered_data.tbr_std_dev)
labels = [str(i)+'+-'+str(j) for i,j in zip(z,z_e)]

coords = list(zip(x,y))

GP = GpRegressor(coords, z, y_err=z_e)

x_gp = linspace(start=min(x), stop=max(x), num=75)
y_gp = linspace(start=min(y), stop=max(y), num=75)

coords_gp = [ (i,j) for i in x_gp for j in y_gp ]

gp_mu, gp_sigma = GP(coords_gp)
gp_mu_folded = np.reshape(gp_mu,(len(x_gp),len(y_gp))).T

traces= []
traces.append(make_2d_surface_trace(gp_mu_folded,x_gp,y_gp,'Tritium Breeding Ratio (TBR)'))   # Makes the actual contours
traces.append(make_2d_scatter_trace(x,y,z,labels))

layout = generate_2d_layout('TBR for '+ blanket_breeder_material +' and ' + blanket_multiplier_material + ' with ' + str(round(blanket_steel_fraction,2)) + ' steel fraction', 
                            'Blanket Breeder Li6 Enrichment Fraction',
                            'breeder / (breeder + multiplier)',x,y)

fig = go.Figure({'data':traces,
                    'layout':layout})
st.write(filtered_data)
st.write('number of data points', len(filtered_data))
# st.write('max tbr (simulated)', max(gp_mu))
st.write('max tbr (fitted)', max(z))
st.write('Plot of matching materials at given steel fraction')
st.write(fig)

#except:
st.write('No available data for criteria')