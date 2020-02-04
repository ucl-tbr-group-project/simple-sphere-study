
import openmc
import streamlit as st

import numpy as np
from neutronics_material_maker import material_maker_classes, Material, MultiMaterial
from tbr_utils import find_tbr_model_sphere_with_no_firstwall

st.write('GUI for performing neutronics simulations')

st.write('Runs simulation using scalable "serverless" solution')

model = st.selectbox('Select neutronics model', 
                      ['sphere with firstwall','sphere with no firstwall'])


materials = st.multiselect(label='Create a material for the breeder zone',
                           options =  list(material_maker_classes.material_dict.keys())
                          )

breeder_materials = []
for material in materials:

    breeder_material = {'material_name' : material}
    if 'packable' in material_maker_classes.material_dict[material].keys():
        if material_maker_classes.material_dict[material]['packable'] == True:
            packing_fraction = st.text_input(label=material + ' packing fraction')
            breeder_material['packing_fraction'] = packing_fraction


    if 'enrichable' in material_maker_classes.material_dict[material].keys():
        if material_maker_classes.material_dict[material]['enrichable'] == True:
            enrichment_fraction = st.text_input(label=material + ' enrichment fraction')
            breeder_material['enrichment_fraction'] = enrichment_fraction

    if 'temperature_in_C' in material_maker_classes.material_dict[material].keys():
        if material_maker_classes.material_dict[material]['temperature_in_C'] == True:
            temperature_in_C = st.text_input(label=material + ' temperature (C)')
            breeder_material['temperature_in_C'] = temperature_in_C

    if len(materials) > 1:
        volume_fraction = st.text_input(label=material + ' volume fraction')
        breeder_material['volume_fraction'] = volume_fraction
    else: breeder_material['volume_fraction'] = 1

    breeder_materials.append(breeder_material)


if st.button('Simulate model'):

    for material in breeder_materials:
        for float_key in ['enrichment_fraction', 'packing_fraction', 'volume_fraction', 'temperature_in_C']:
            if float_key in material.keys():
                material[float_key] = float(material[float_key])

    if len(materials) == 1:
        for material in breeder_materials:
            breeder_material = Material(**material).neutronics_material
        tbr = find_tbr_model_sphere_with_no_firstwall(breeder_material)
        st.write('tbr',tbr)

    else:
        multimaterials = []
        volume_fractions = []
        for material in breeder_materials:
            multimaterials.append(Material(**material))
            volume_fractions.append(material['volume_fraction'])
        breeder_material = MultiMaterial(material_name='breeder_material', materials=multimaterials, volume_fractions=volume_fractions).neutronics_material
        print(breeder_material)
        tbr = find_tbr_model_sphere_with_no_firstwall(breeder_material)
        st.write('tbr',tbr)
 
