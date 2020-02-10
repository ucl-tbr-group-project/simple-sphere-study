
import os

import numpy as np
import openmc
import streamlit as st

from neutronics_material_maker import (Material, MultiMaterial,
                                       material_maker_classes)
from tbr_utils import (find_tbr_model_sphere_with_firstwall,
                       find_tbr_model_sphere_with_no_firstwall)

st.write('GUI for performing neutronics simulations')

st.write('Runs simulation using scalable "serverless" solution')

model = st.selectbox('Select neutronics model',
                     ['sphere with firstwall', 'sphere with no firstwall'])

if model == 'sphere with firstwall':
   st.image('images/sphere_with_firstwall.png', width=500)
if model == 'sphere with no firstwall':
   st.image('images/sphere_with_no_firstwall.png', width=500)


st.write('BLANKET')

materials = st.multiselect(label='Create a material for the breeder zone',
                           options =  list(material_maker_classes.material_dict.keys())
                           )

breeder_materials = []
for material in materials:

    # keys are required in the text_inputs to allow same materials to be chosen for both breeder and firstwall (gives unique identifier to that material for that component)
    # i.e. materials in the same component can have the same key because they only appear once in the component
    # but the same material must have different keys in different components to keep track
    # materials in the blanket have the key = 'breeder'
    # materials in the firstwall have the key = 'firstwall'

    breeder_material = {'material_name' : material}
    if 'packable' in material_maker_classes.material_dict[material].keys():
        if material_maker_classes.material_dict[material]['packable'] == True:
            packing_fraction = st.text_input(key='breeder', label=material + ' packing fraction')  # key is required to allow same materials to be chosen for both breeder and firstwall
            breeder_material['packing_fraction'] = packing_fraction

    if 'enrichable' in material_maker_classes.material_dict[material].keys():
        if material_maker_classes.material_dict[material]['enrichable'] == True:
            enrichment_fraction = st.text_input(key='breeder', label=material + ' enrichment fraction')
            breeder_material['enrichment_fraction'] = enrichment_fraction

    if 'temperature_in_C' in material_maker_classes.material_dict[material].keys():
        if material_maker_classes.material_dict[material]['temperature_in_C'] == True:
            temperature_in_C = st.text_input(key='breeder', label=material + ' temperature (C)')
            breeder_material['temperature_in_C'] = temperature_in_C

    if len(materials) > 1:
        volume_fraction = st.text_input(key='breeder', label=material + ' volume fraction')
        breeder_material['volume_fraction'] = volume_fraction
    else: breeder_material['volume_fraction'] = 1

    breeder_materials.append(breeder_material)

if model == 'sphere with firstwall':

    st.write('FIRSTWALL')

    fw_thickness = st.text_input(label='Select firstwall thickness')

    fw_materials = st.multiselect(label='Create a material for the firstwall',
                                  options = list(material_maker_classes.material_dict.keys())
                                  )

    firstwall_materials = []
    for material in fw_materials:

        fw_material = {'material_name' : material}
        if 'packable' in material_maker_classes.material_dict[material].keys():
            if material_maker_classes.material_dict[material]['packable'] == True:
                packing_fraction = st.text_input(key='firstwall', label=material + ' packing fraction')
                fw_material['packing_fraction'] = packing_fraction

        if 'enrichable' in material_maker_classes.material_dict[material].keys():
            if material_maker_classes.material_dict[material]['enrichable'] == True:
                enrichment_fraction = st.text_input(key='firstwall', label=material + ' enrichment fraction')
                fw_material['enrichment_fraction'] = enrichment_fraction

        if 'temperature_in_C' in material_maker_classes.material_dict[material].keys():
            if material_maker_classes.material_dict[material]['temperature_in_C'] == True:
                temperature_in_C = st.text_input(key='firstwall', label=material + ' temperature (C)')
                fw_material['temperature_in_C'] = temperature_in_C

        if len(fw_materials) > 1:
            volume_fraction = st.text_input(key='firstwall', label=material + ' volume fraction')
            fw_material['volume_fraction'] = volume_fraction
        else: fw_material['volume_fraction'] = 1

        firstwall_materials.append(fw_material)



if st.button('Simulate model'):

    for material in breeder_materials:
        for float_key in ['enrichment_fraction', 'packing_fraction', 'volume_fraction', 'temperature_in_C']:
            if float_key in material.keys():
                material[float_key] = float(material[float_key])

    if len(materials) == 1:
        for material in breeder_materials:
            breeder_material = Material(**material).neutronics_material

    else:
        multimaterials = []
        volume_fractions = []
        for material in breeder_materials:
            multimaterials.append(Material(**material))
            volume_fractions.append(material['volume_fraction'])
        breeder_material = MultiMaterial(material_name='breeder_material', materials=multimaterials, volume_fractions=volume_fractions).neutronics_material


    if model == 'sphere with firstwall':
        for material in firstwall_materials:
            for float_key in ['enrichment_fraction', 'packing_fraction', 'volume_fraction', 'temperature_in_C']:
                if float_key in material.keys():
                    material[float_key] = float(material[float_key])

        if len(firstwall_materials) == 1:
            for material in firstwall_materials:
                firstwall_material = Material(**material).neutronics_material
        else:
            multimaterials = []
            volume_fractions = []
            for material in firstwall_materials:
                multimaterials.append(Material(**material))
                volume_fractions.append(material['volume_fraction'])
            firstwall_material = MultiMaterial(material_name='firstwall_material', materials=multimaterials, volume_fractions=volume_fractions).neutronics_material

        tbr = find_tbr_model_sphere_with_firstwall(breeder_material, firstwall_material, float(fw_thickness))
        st.write('tbr', tbr)

    else:
        print(breeder_material)
        tbr = find_tbr_model_sphere_with_no_firstwall(breeder_material)
        st.write('tbr', tbr)
