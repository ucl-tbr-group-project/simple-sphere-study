
import streamlit as st
import json
import pandas as pd
import numpy as np

st.title('Simple TBR Simulator')

@st.cache
def load_data():
    return pd.read_json('results.json') 

data = load_data()

# st.write(data[0])

st.write(data.keys())
firstwall_coolant = st.selectbox('select a firstwall coolant', data['firstwall_coolant'].unique())
blanket_multiplier_material = st.selectbox('select a blanket multiplier material', data['blanket_multiplier_material'].unique())
blanket_breeder_material = st.selectbox('select a blanket multiplier material', data['blanket_breeder_material'].unique())


# coolant = st.selectbox('select field', data.keys())
# st.bar_chart(np.histogram(data['tbr'].values))

tbr_values = st.slider( 'Required TBR value', 0.0, 2.0, (1., 2.))
blanket_steel_fraction = st.slider( 'select a range of blanket steel fractions', 0.0, 1.0, (0., 1.))
blanket_multiplier_fraction = st.slider( 'select a range of blanket multiplier fractions', 0.0, 1.0, (0., 1.))
blanket_breeder_fraction = st.slider( 'select a range of blanket breeder fractions', 0.0, 1.0, (0., 1.))
blanket_breeder_fraction = st.slider( 'select a range of lithium 6 enrichment fractions', 0.0, 1.0, (0., 1.))

st.write('Simulations that meet these criteria')

filtered_data = data[
                     (data.firstwall_coolant == firstwall_coolant) & 
                     (data.blanket_multiplier_material == blanket_multiplier_material)
                    ]

st.write(filtered_data)