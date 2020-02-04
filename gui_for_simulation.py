
import openmc
import streamlit as st

import numpy as np
from neutronics_material_maker import material_maker_classes, Material, MultiMaterial
from tbr_utils import find_tbr_model_sphere_with_no_firstwall

# from paramak import Shape, Reactor
# from neutronics_material_maker import Material, MultiMaterial
# from paramak.find_coordinates.find_plasma_coordinates import *


# Define model

st.write('GUI for performing neutronics simulations')

st.write('Runs simulation using scalable "serverless" solution')

# model = st.selectbox('Select neutronics model', 
#                       model_names = ['sphere with firstwall','sphere with no firstwall'])

print(list(material_maker_classes.material_dict.keys()))

materials = st.multiselect(label='Create a material for the breeder zone',
                           options =  list(material_maker_classes.material_dict.keys())
                          )

breeder_materials = []
for material in materials:

    breeder_material = {'material_name' : material}
    volume_fraction = st.text_input(label=material + ' volume fraction')
    breeder_material['volume_fraction'] = volume_fraction
    if 'packable' in material_maker_classes.material_dict[material].keys():
        if material_maker_classes.material_dict[material]['packable'] == True:
            packing_fraction = st.text_input(label=material + ' packing fraction')
            breeder_material['packing_fraction'] = packing_fraction
        else: breeder_material['packing_fraction'] = 0
    else: breeder_material['packing_fraction'] = 0
    if 'enrichable' in material_maker_classes.material_dict[material].keys():
        if material_maker_classes.material_dict[material]['enrichable'] == True:
            enrichment_fraction = st.text_input(label=material + ' enrichment fraction')
            breeder_material['enrichment_fraction'] = enrichment_fraction
        else: breeder_material['enrichment_fraction'] = 0
    else: breeder_material['enrichment_fraction'] = 0
    breeder_materials.append(breeder_material)


if st.button('make material'):

    if len(materials) == 1:
        for material in breeder_materials:
            breeder_material = Material(material_name=material['material_name'], packing_fraction=float(material['packing_fraction']), enrichment_fraction=float(material['enrichment_fraction'])).neutronics_material
        tbr = find_tbr_model_sphere_with_no_firstwall(breeder_material)
        st.write('tbr',tbr)

    else:
        multimaterials = []
        volume_fractions = []
        for material in breeder_materials:
            multimaterials.append(Material(material_name=material['material_name'], packing_fraction=float(material['packing_fraction']), enrichment_fraction=float(material['enrichment_fraction'])))
            volume_fractions.append(float(material['volume_fraction']))
        breeder_material = MultiMaterial(material_name='breeder_material', materials=multimaterials, volume_fractions=volume_fractions).neutronics_material
        print(breeder_material)
        tbr = find_tbr_model_sphere_with_no_firstwall(breeder_material)
        st.write('tbr',tbr)
 





# required_inputs = {
#                     'sphere with no firstwall':['blanket_structural_material',
#                                                 'blanket_structural_fraction',
#                                                 'blanket_coolant_material',
#                                                 'blanket_coolant_fraction',
#                                                 'blanket_multiplier_fraction',
#                                                 'blanket_multiplier_material',
#                                                 'blanket_breeder_fraction',
#                                                 'blanket_breeder_material',
#                                                 'blanket_breeder_li6_enrichment_fraction',
#                                                 'blanket_breeder_packing_fraction',
#                                                 'blanket_multiplier_packing_fraction'
#                                                 ]
# }

# description_of_inputs = {'blanket_structural_material':'selectbox',
#                          'blanket_structural_fraction':'slider',
#                          'blanket_coolant_material':'selectbox',
#                          'blanket_coolant_fraction':'slider',
#                          'blanket_multiplier_fraction':'slider',
#                          'blanket_multiplier_material':'selectbox',
#                          'blanket_breeder_fraction':'slider',
#                          'blanket_breeder_material':'selectbox',
#                          'blanket_breeder_li6_enrichment_fraction':'slider',
#                          'blanket_breeder_packing_fraction':'slider',
#                          'blanket_multiplier_packing_fraction':'slider'
#                          }

# contents_of_inputs = {'blanket_structural_material':['eurofer','steel'],
#                         'blanket_structural_fraction':[0,1],
#                         'blanket_coolant_material':['eurofer','steel'],
#                         'blanket_coolant_fraction':[0,1],
#                         'blanket_multiplier_fraction':[0,1],
#                         'blanket_multiplier_material':['eurofer','steel'],
#                         'blanket_breeder_fraction':[0,1],
#                         'blanket_breeder_material':['eurofer','steel'],
#                         'blanket_breeder_li6_enrichment_fraction':[0,1],
#                         'blanket_breeder_packing_fraction':[0,1],
#                         'blanket_multiplier_packing_fraction':[0,1]
#                          }


# if model == None:
#     pass
# else:





# for material in material_identities:
#     material_selection = st.selectbox('Select blanket '+material, list(material_dict.keys()))

#     if material_selection in model_materials:
#         st.write('Please select a different material')

#     else:
#         model_materials.append(material_selection)

#         if 'enrichable' in material_dict[material_selection].keys():
#             if material_dict[material_selection]['enrichable']==True:
#                 material_enrichment = st.slider('Select ' + material_selection + ' enrichment', min_value=0.0, max_value=1.0, step=0.01)
#                 model_materials_enrichments.append(material_enrichment)
#             else:
#                 material_enrichment = 0.0
#                 model_materials_enrichments.append(material_enrichment)
#         else:
#             material_enrichment = 0.0
#             model_materials_enrichments.append(material_enrichment)


#         if 'packable' in material_dict[material_selection].keys():
#             if material_dict[material_selection]['packable']==True:
#                 packing_fraction = st.slider('Select ' + material_selection + ' packing fraction', min_value=0.0, max_value=1.0, value=1.0, step=0.01)
#                 model_packing_fractions.append(packing_fraction)
#             else:
#                 packing_fraction = 1.0
#                 model_packing_fractions.append(packing_fraction)
#         else:
#             packing_fraction = 1.0
#             model_packing_fractions.append(packing_fraction)


#         if number_of_blanket_materials == 1:
#             vol_fraction = 1
#             model_volume_fractions.append(vol_fraction)

#         else:
#             vol_fraction = st.text_input('Enter ' + material_selection + ' volume fraction')
#             if vol_fraction == '':
#                 pass
#             else:
#                 try:
#                     if 0 <= float(vol_fraction) <= 1:
#                         st.write(material_selection + ' volume fraction = ' + vol_fraction)
#                         model_volume_fractions.append(float(vol_fraction))
#                     else:
#                         st.write('Volume fraction must be between 0 and 1')
#                 except ValueError:
#                     st.write('Please enter a valid volume fraction')

# multimaterial_materials = []

# try:
#     for i, j, k in zip(model_materials, model_materials_enrichments, model_packing_fractions):
#         multimaterial_materials.append(Material(i, enrichment_fraction=j, packing_fraction=k, temperature_in_C=temp_in_C))
# except NameError:
#     pass
#     # this is checked later on

# blanket_material = MultiMaterial(material_name='blanket_material', materials=multimaterial_materials, volume_fractions=model_volume_fractions)


# if st.button('Run simulation'):

#     if len(temperature) != 1:
#         raise ValueError('Valid temperature has not been entered')

#     if len(model_materials) != number_of_blanket_materials:
#         raise ValueError('Error constructing blanket material')

#     if sum(model_volume_fractions) != 1:
#         raise ValueError('Volume fractions must sum to 1')


#     # specify model materials (once tests are complete)
#     centre_column.material = centre_column_material
#     blanket.material = blanket_material

#     # tallies
#     blanket.add_tally('(n,Xt)')
#     blanket.add_tally('(n,heating)')
#     blanket.add_tally('(p,heating)')

#     # make reactor
#     myreactor = Reactor()
#     myreactor['blanket'] = blanket
#     myreactor['centre_column'] = centre_column

#     myreactor.export_stp()
#     myreactor.export_neutronics_model(plasma)
#     # myreactor.createNeutronicsMaterials() # this command is no longer needed
#     myreactor.simulate_neutronics_model()
#     print(myreactor.tally_results)

