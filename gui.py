import streamlit as st
import json
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from plotly.offline import download_plotlyjs, plot
from plotly.graph_objs import Scatter, Layout
import plotly.graph_objects as go

st.title('Simple TBR Simulator')

@st.cache
def load_data():
    return pd.read_json('results.json') 

data = load_data()

# st.write(data[0])

st.write(data.keys())
firstwall_coolant = st.selectbox('select a firstwall coolant', data['firstwall_coolant'].unique())
blanket_multiplier_material = st.selectbox('select a blanket multiplier material', data['blanket_multiplier_material'].unique())
blanket_breeder_material = st.selectbox('select a blanket breeder material', data['blanket_breeder_material'].unique())


# coolant = st.selectbox('select field', data.keys())
# st.bar_chart(np.histogram(data['tbr'].values))

# tbr_values = st.slider( 'Required TBR value', 0.0, 2.0, (1., 2.))
# blanket_steel_fraction = st.slider( 'select a range of blanket steel fractions', 0.0, 1.0, (0., 1.))
# blanket_multiplier_fraction = st.slider( 'select a range of blanket multiplier fractions', 0.0, 1.0, (0., 1.))
# blanket_breeder_fraction = st.slider( 'select a range of blanket breeder fractions', 0.0, 1.0, (0., 1.))
# blanket_enrichment_fraction = st.slider( 'select a range of lithium 6 enrichment fractions', 0.0, 1.0, (0., 1.))

tbr_values = st.slider('Required TBR value', min_value=0.0, max_value=2.0, value=(0., 2.))
blanket_steel_fraction = st.slider('Select a range of blanket steel fractions', min_value=0.0, max_value=1.0, value=(0.,1.))
blanket_multiplier_fraction = st.slider('Select a range of blanket multiplier fractions', min_value=0.0, max_value=1.0, value=(0.,1.))
blanket_breeder_fraction = st.slider('Select a range of blanket breeder fractions', min_value=0.0, max_value=1.0, value=(0.,1.))
blanket_enrichment_fraction = st.slider('Select a range of lithium 6 enrichment fractions', min_value=0.0, max_value=1.0, value=(0.,1.))

st.write('Simulations that meet these criteria')

filtered_data = data[
                     (data.firstwall_coolant == firstwall_coolant) & 
                     (data.blanket_multiplier_material == blanket_multiplier_material) &
                     (data.blanket_breeder_material == blanket_breeder_material) &
                     (data.tbr >= tbr_values[0]) & (data.tbr <= tbr_values[1]) &
                     (data.blanket_steel_fraction >= blanket_steel_fraction[0]) & (data.blanket_steel_fraction <= blanket_steel_fraction[1]) &
                     (data.blanket_multiplier_fraction >= blanket_multiplier_fraction[0]) & (data.blanket_multiplier_fraction <= blanket_multiplier_fraction[1]) &
                     (data.blanket_breeder_fraction >= blanket_breeder_fraction[0]) & (data.blanket_breeder_fraction <= blanket_breeder_fraction[1]) &
                     (data.blanket_breeder_li6_enrichment_fraction >= blanket_enrichment_fraction[0]) & (data.blanket_breeder_li6_enrichment_fraction <= blanket_enrichment_fraction[1])
                    ]

st.write(filtered_data)

traces = []

layout = Layout(xaxis={'title':'BLANKET MULTIPLIER FRACTION',
                       'showline':True,
                       'range':(0., 1.),
                       },
                yaxis={'title':'TBR',
                       },
                title='TEST GRAPH ILLUSTRATION',
                hovermode='closest'
                )

traces.append(Scatter(x=filtered_data.blanket_multiplier_fraction,
                      y=filtered_data.tbr,
                      mode='markers'))

fig = go.Figure({'data':traces,
                 'layout':layout})

st.write(fig)