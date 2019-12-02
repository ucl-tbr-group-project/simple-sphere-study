
import streamlit as st
import json
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.title('TBR results explorer')

@st.cache
def load_data():
    return pd.read_json('results.json') 

data = load_data()

# st.write(data[0])

st.write(data.keys())
st.write('Firstwall coolants')
firstwall_coolants = data['firstwall_coolant'].unique()
selected_firstwall_coolants = []
for firstwall_coolant in firstwall_coolants:
    is_selected = st.checkbox(label=firstwall_coolant, value=True)
    if is_selected == True:
        selected_firstwall_coolants.append(firstwall_coolant)

st.write('blanket multiplier materials')
blanket_multiplier_materials = data['blanket_multiplier_material'].unique()
selected_blanket_multiplier_materials=[]
for blanket_multiplier_material in blanket_multiplier_materials:
    is_selected = st.checkbox(label=blanket_multiplier_material, value=True)
    if is_selected == True:
        selected_blanket_multiplier_materials.append(blanket_multiplier_material)
print(selected_blanket_multiplier_materials)

# coolant = st.selectbox('select field', data.keys())
# st.bar_chart(np.histogram(data['tbr'].values))

tbr_values = st.slider( 'Required TBR value', 0.0, 2.0, (1., 2.))
blanket_steel_fraction = st.slider( 'select a range of blanket steel fractions', 0.0, 1.0, (0., 1.))
blanket_multiplier_fraction = st.slider( 'select a range of blanket multiplier fractions', 0.0, 1.0, (0., 1.))
blanket_breeder_fraction = st.slider( 'select a range of blanket breeder fractions', 0.0, 1.0, (0., 1.))
blanket_breeder_fraction = st.slider( 'select a range of lithium 6 enrichment fractions', 0.0, 1.0, (0., 1.))

st.write('Simulations that meet these criteria')

filtered_data = data[
                     (data.firstwall_coolant.isin(selected_firstwall_coolants)) & 
                     (data.blanket_multiplier_material.isin(selected_blanket_multiplier_materials))
                    ]

st.write(filtered_data)

x_data = filtered_data.blanket_breeder_material.unique()
print(x_data)
# x_data = ['Carmelo Anthony', 'Dwyane Wade']

N = 50

y0 = (10 * np.random.randn(N) + 30).astype(np.int)
y1 = (13 * np.random.randn(N) + 38).astype(np.int)

colors = ['rgba(93, 164, 214, 0.5)', 'rgba(255, 144, 14, 0.5)']

fig = go.Figure()

y_data = []
for breeder_material in filtered_data.blanket_breeder_material.unique():
    y_data.append(
                  data[
                        (data.blanket_breeder_material == breeder_material) &
                        (data.firstwall_coolant.isin(selected_firstwall_coolants)) & 
                        (data.blanket_multiplier_material.isin(selected_blanket_multiplier_materials))
                        ]['tbr']
                 )
    print(y_data)

for entry in y_data:
    fig.add_trace(go.Histogram(x=entry,
                            xbins=dict( # bins used for histogram
                                            start=0,
                                            end=2.0,
                                            size=0.1
                                        ),
                            )
                )

fig.update_layout(barmode='overlay')  
fig.update_traces(opacity=0.75)


st.write(fig)