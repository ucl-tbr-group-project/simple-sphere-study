
import streamlit as st
import json
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.title('TBR results explorer')

@st.cache
def load_data():
    return pd.read_json('results_grid3.json') 

data = load_data()

catorgorical_key_names = [
                          'firstwall_amour_material',
                          'firstwall_structural_material',
                          'firstwall_coolant_material'
                         ]
selected_catorgorical_key_names = {}

for key_name in catorgorical_key_names:
        st.write(key_name.replace('_',' '))
        selected = []
        for material in data[key_name].unique():
                is_selected = st.checkbox(label=material, value=False)
                if is_selected == True:
                        selected.append(material)
        selected_catorgorical_key_names[key_name] = selected

print(selected_catorgorical_key_names)

# 'Blanket only' image is displayed only when 'no firstwall' is selected - i.e. when only the model without a blanket is used
# 'Blanket AND first wall' image is displayed when ONLY 'H2O' and/or 'He' are selected - i.e. when only model WITH blanket is used
# 'Placeholder' image is displayed when 'no firstwall' AND ('H2O' or 'He') are selected - i.e. when both models are used
# Image path specified with respect to current directory

# try:
#         if selected_firstwall_coolants[0] == "no firstwall":
#                 try:
#                         if len(selected_firstwall_coolants) >= 1:
#                                 st.image('./images/placeholder_image.png')

#                 except IndexError:
#                         st.image('./images/blanket_only.png')

#         else:
#                 st.image('./images/blanket_and_fw.png')

# except IndexError:
#         st.write('Please select firstwall criteria')


# tbr_values = st.slider( 'Required TBR value', 0.0, 3., (0., 3.))
# blanket_structural_fractions = st.slider( 'select a range of blanket structural fractions', 0.0, 1.0, (0., 1.))
# blanket_coolant_fractions = st.slider( 'select a range of blanket breeder fractions', 0.0, 1.0, (0., 1.))
# blanket_multiplier_fractions = st.slider( 'select a range of blanket multiplier fractions', 0.0, 1.0, (0., 1.))
# blanket_breeder_fractions = st.slider( 'select a range of blanket breeder fractions', 0.0, 1.0, (0., 1.))
# blanket_enrichment_fractions = st.slider( 'select a range of lithium 6 enrichment fractions', 0.0, 1.0, (0., 1.))



# filtered_data = data[
#                 (data.selected_firstwall_amour_material.isin(selected_firstwall_amour_materials)) & 
#                 (data.selected_firstwall_coolants.isin(selected_firstwall_coolants)) & 
#                 (data.firstwall_coolant.isin(selected_firstwall_coolants)) & 
#                 (data.blanket_breeder_material.isin(selected_blanket_breeder_materials)) &
#                 (data.blanket_multiplier_material.isin(selected_blanket_multiplier_materials)) & 
#                 (data.tbr >= tbr_values[0]) & (data.tbr <= tbr_values[1]) &
#                 (data.blanket_structural_fraction >= blanket_structural_fractions[0]-0.001) & (data.blanket_steel_fraction <= blanket_steel_fractions[1]+0.001) &
#                 (data.blanket_multiplier_fraction >= blanket_multiplier_fractions[0]) & (data.blanket_multiplier_fraction <= blanket_multiplier_fractions[1]) &
#                 (data.blanket_breeder_fraction >= blanket_breeder_fractions[0]) & (data.blanket_breeder_fraction <= blanket_breeder_fractions[1]) &
#                 (data.blanket_breeder_li6_enrichment_fraction >= blanket_enrichment_fractions[0]) & (data.blanket_breeder_li6_enrichment_fraction <= blanket_enrichment_fractions[1])
#                 ]

# if len(filtered_data) == 0:
#         st.write('No simulations matching criteria')

# else:


#         st.write(' Number of simulations matching criteria ' ,len(filtered_data))
#         st.write(filtered_data)

#         colors = ['rgba(93, 164, 214)', 'rgba(255, 144, 14)']

#         fig = go.Figure()
#         for c, breeder_material in zip(colors, selected_blanket_breeder_materials):

#                 y_data = filtered_data[(filtered_data.blanket_breeder_material == breeder_material)]['tbr']
                                
#                 fig.add_trace(go.Histogram(x=y_data,
#                                         name= breeder_material,
#                                         xbins=dict(start=0),
#                                         marker_line_width=1.5
#                                         )
#                                 )


#         fig.update_layout(barmode='overlay',
#                         xaxis_title="TBR",
#                         yaxis_title="number of simulations",
#                         title="Impact of Breeder Material",               
#                         )    
#         fig.update_traces(opacity=0.4)
#         st.write(fig)
#         for breeder_material in selected_blanket_breeder_materials:
#                 y_data = filtered_data[(filtered_data.blanket_breeder_material == breeder_material)]['tbr']
#                 if len(y_data) != 0:                
#                         st.write(' Maximum TBR for ' ,breeder_material, ' = ',max(y_data) )




#         fig = go.Figure()
#         for multiplier_material in selected_blanket_multiplier_materials:

#                 y_data = filtered_data[(filtered_data.blanket_multiplier_material == multiplier_material)]['tbr']
                                
#                 fig.add_trace(go.Histogram(x=y_data,
#                                         name= multiplier_material,
#                                         xbins=dict(start=0),
#                                         marker_line_width=1.5
#                                         )
#                                 )

#         fig.update_layout(barmode='overlay',
#                         xaxis_title="TBR",
#                         yaxis_title="number of simulations",
#                         title="Impact of Multiplier Material")    
#         fig.update_traces(opacity=0.4)
#         st.write(fig)
#         for multiplier_material in selected_blanket_multiplier_materials:
#                 y_data = filtered_data[(filtered_data.blanket_multiplier_material == multiplier_material)]['tbr']
#                 if len(y_data) != 0:                
#                         st.write(' Maximum TBR for ' ,multiplier_material, ' = ',max(y_data) )



#         fig = go.Figure()
#         for firstwall_coolant in selected_firstwall_coolants:

#                 y_data = filtered_data[(filtered_data.firstwall_coolant == firstwall_coolant)]['tbr']
                                
#                 fig.add_trace(go.Histogram(x=y_data,
#                                         name= firstwall_coolant,
#                                         xbins=dict(start=0),
#                                         marker_line_width=1.5
#                                         )
#                                 )


#         fig.update_layout(barmode='overlay',
#                         xaxis_title="TBR",
#                         yaxis_title="number of simulations",
#                         title="Impact of Firstwall Coolant")  
#         fig.update_traces(opacity=0.4)
#         st.write(fig)
#         for firstwall_coolant in selected_firstwall_coolants:
#                 y_data = filtered_data[(filtered_data.firstwall_coolant == firstwall_coolant)]['tbr']
#                 if len(y_data) != 0:
#                         st.write(' Maximum TBR for ' ,firstwall_coolant, ' = ',max(y_data) )