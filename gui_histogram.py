
import streamlit as st
import json
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.title('TBR results explorer')

@st.cache
def load_data():
    return pd.read_json('results_hom.json') 

data = load_data()


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


st.write('blanket breeder materials')
blanket_breeder_materials = data['blanket_breeder_material'].unique()
selected_blanket_breeder_materials=[]
for blanket_breeder_material in blanket_breeder_materials:
    is_selected = st.checkbox(label=blanket_breeder_material, value=True)
    if is_selected == True:
        selected_blanket_breeder_materials.append(blanket_breeder_material)
print(selected_blanket_breeder_materials)


tbr_values = st.slider( 'Required TBR value', 0.0, 2.0, (1., 2.))
blanket_steel_fractions = st.slider( 'select a range of blanket steel fractions', 0.0, 1.0, (0., 1.))
blanket_multiplier_fractions = st.slider( 'select a range of blanket multiplier fractions', 0.0, 1.0, (0., 1.))
blanket_breeder_fractions = st.slider( 'select a range of blanket breeder fractions', 0.0, 1.0, (0., 1.))
blanket_enrichment_fractions = st.slider( 'select a range of lithium 6 enrichment fractions', 0.0, 1.0, (0., 1.))



filtered_data = data[
                     (data.firstwall_coolant.isin(selected_firstwall_coolants)) & 
                     (data.blanket_breeder_material.isin(selected_blanket_breeder_materials)) &
                     (data.blanket_multiplier_material.isin(selected_blanket_multiplier_materials)) & 
                     (data.tbr >= tbr_values[0]) & (data.tbr <= tbr_values[1]) &
                     (data.blanket_steel_fraction >= blanket_steel_fractions[0]-0.001) & (data.blanket_steel_fraction <= blanket_steel_fractions[1]+0.001) &
                     (data.blanket_multiplier_fraction >= blanket_multiplier_fractions[0]) & (data.blanket_multiplier_fraction <= blanket_multiplier_fractions[1]) &
                     (data.blanket_breeder_fraction >= blanket_breeder_fractions[0]) & (data.blanket_breeder_fraction <= blanket_breeder_fractions[1]) &
                     (data.blanket_breeder_li6_enrichment_fraction >= blanket_enrichment_fractions[0]) & (data.blanket_breeder_li6_enrichment_fraction <= blanket_enrichment_fractions[1])
                    ]

st.write(' Number of simulations matching criteria ' ,len(filtered_data))
st.write(filtered_data)

colors = ['rgba(93, 164, 214, 0.5)', 'rgba(255, 144, 14, 0.5)']

fig = go.Figure()

y_data = []
for breeder_material in selected_blanket_breeder_materials:
    y_data.append(
                  filtered_data[
                        (filtered_data.blanket_breeder_material == breeder_material)
                      ]['tbr']
                 )
    print(y_data)

for entry, breeder_material in zip(y_data, selected_blanket_breeder_materials):
    fig.add_trace(go.Histogram(x=entry,
                               name= breeder_material,
                               xbins=dict( # bins used for histogram
                                               start=0,
                                            #    end=2.5,
                                               # size=0.1
                                         ),
                              )
                )
    try:
        st.write(' Maximum TBR for ' ,breeder_material, ' = ',max(entry) )
    except:
        pass

fig.update_layout(barmode='overlay',
                 xaxis_title="TBR",
    yaxis_title="number",)  
fig.update_traces(opacity=0.75)


st.write(fig)