from flask import Flask, jsonify, make_response, request
import json
from tbr_utils import find_tbr
import random
import numpy as np

application = Flask(__name__)

model_names = ['sphere_with_firstwall', 'sphere_with_no_firstwall']
firstwall_coolant_material_options = ['H2O', 'He', 'D2O']
blanket_coolant_material_options = ['H2O', 'He', 'D2O']
blanket_multiplier_material_options = ['Be', 'Be12Ti']
blanket_breeder_material_options = ['Li4SiO4','Li2TiO3']
blanket_structural_material_options = ['SiC','eurofer']
firstwall_amour_material_options = ['tungsten']
firstwall_structural_material_options = ['SiC','eurofer']
firstwall_thicknesses = np.linspace(start=0.5, stop=5., num=10, endpoint=True).tolist()
firstwall_amour_fraction = 0.055262
firstwall_structural_fraction = 0.253962
firstwall_coolant_fraction = 0.690776

blanket_breeder_li6_enrichment_fractions = np.linspace(start=0., stop=1., num=10, endpoint=True).tolist()
blanket_breeder_li6_enrichment_fractions.append(0.0759)
blanket_breeder_packing_fractions = np.linspace(start=0.6, stop=1., num=10, endpoint=True).tolist()
blanket_multiplier_packing_fractions = np.linspace(start=0.6, stop=1., num=10, endpoint=True).tolist()


for i in range(50):
    blanket_fractions = np.random.dirichlet(np.ones(4),size=1)

@application.route('/' ,methods=['GET','POST'])
def return_help():
    return 'try /find_tbr'


@application.route('/find_tbr' ,methods=['GET','POST'])
def call_find_tbr():

    model_name = random.choice(model_names)

    firstwall_thickness = random.choice(firstwall_thicknesses)
    firstwall_amour_material = random.choice(firstwall_amour_material_options)
    firstwall_structural_material = random.choice(firstwall_structural_material_options)
    firstwall_coolant_material = random.choice(firstwall_coolant_material_options)

    blanket_structural_material = random.choice(blanket_structural_material_options)
    blanket_breeder_material = random.choice(blanket_breeder_material_options)
    blanket_multiplier_material = random.choice(blanket_multiplier_material_options)
    blanket_coolant_material = random.choice(blanket_coolant_material_options)

    blanket_breeder_li6_enrichment_fraction = random.choice(blanket_breeder_li6_enrichment_fractions)
    blanket_breeder_packing_fraction = random.choice(blanket_breeder_packing_fractions)
    blanket_multiplier_packing_fraction = random.choice(blanket_multiplier_packing_fractions)

    selected_blanket_fractions = random.choice(blanket_fractions)
    blanket_multiplier_fraction = selected_blanket_fractions[0]
    blanket_breeder_fraction = selected_blanket_fractions[1]
    blanket_structural_fraction = selected_blanket_fractions[2]
    blanket_coolant_fraction = selected_blanket_fractions[3]

    model_name = request.args.get('model_name', 
                                  type=str,
                                  default=model_name
                                  )

    print('model_name', model_name)
 
    firstwall_structural_material = request.args.get(firstwall_structural_material, 
                                                     type=str,
                                                     default=firstwall_structural_material
                                                     )

    inputs_and_results = find_tbr( model_name=model_name,
                                    firstwall_thickness=firstwall_thickness,
                                    firstwall_amour_material=firstwall_amour_material,
                                    firstwall_amour_fraction=firstwall_amour_fraction,
                                    firstwall_structural_material=firstwall_structural_material,
                                    firstwall_structural_fraction=firstwall_structural_fraction,
                                    firstwall_coolant_material=firstwall_coolant_material,
                                    firstwall_coolant_fraction=firstwall_coolant_fraction,
                                    blanket_structural_material=blanket_structural_material,
                                    blanket_structural_fraction=blanket_structural_fraction,
                                    blanket_coolant_material=blanket_coolant_material,
                                    blanket_coolant_fraction=blanket_coolant_fraction,
                                    blanket_multiplier_fraction=blanket_multiplier_fraction,
                                    blanket_multiplier_material=blanket_multiplier_material,
                                    blanket_breeder_fraction=blanket_breeder_fraction,
                                    blanket_breeder_material=blanket_breeder_material,
                                    blanket_breeder_li6_enrichment_fraction=blanket_breeder_li6_enrichment_fraction,
                                    blanket_breeder_packing_fraction=blanket_breeder_packing_fraction,
                                    blanket_multiplier_packing_fraction=blanket_multiplier_packing_fraction,
    
    )
    print(inputs_and_results)
    
    return inputs_and_results    

if __name__ == '__main__':
    application.run(
        #debug=True,
        host='0.0.0.0',
        port=8080,
        # ssl_context=context
    )