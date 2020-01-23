from flask import Flask, jsonify, make_response, request
import json
from tbr_utils import find_tbr_model_sphere_with_firstwall, find_tbr_model_sphere_with_no_firstwall
import random
import numpy as np

application = Flask(__name__)


firstwall_amour_material_options = ['tungsten']
firstwall_structural_material_options = ['SiC','eurofer']
firstwall_thicknesses = np.linspace(start=0.5, stop=5., num=10, endpoint=True).tolist()
firstwall_amour_fraction = 0.055262
firstwall_structural_fraction = 0.253962
firstwall_coolant_fraction = 0.690776
firstwall_coolant_material_options = ['H2O', 'He', 'D2O']
blanket_coolant_material_options = ['H2O', 'He', 'D2O']
blanket_multiplier_material_options = ['Be', 'Be12Ti']
blanket_breeder_material_options = ['Li4SiO4','Li2TiO3']
blanket_structural_material_options = ['SiC','eurofer']

blanket_breeder_li6_enrichment_fractions = np.linspace(start=0., stop=1., num=10, endpoint=True).tolist()
blanket_breeder_li6_enrichment_fractions.append(0.0759)
blanket_breeder_packing_fractions = np.linspace(start=0.6, stop=1., num=10, endpoint=True).tolist()
blanket_multiplier_packing_fractions = np.linspace(start=0.6, stop=1., num=10, endpoint=True).tolist()


for i in range(50):
    blanket_fractions = np.random.dirichlet(np.ones(4),size=1)

help_hints = 'try a different url endpoint <br> \
            <br> \
            <br> \
            URL endpoint with optional arguments <br> \
            /find_tbr_model_sphere_with_firstwall <br> \
            firstwall_thickness <br> \
            firstwall_amour_material <br> \
            firstwall_structural_material <br> \
            firstwall_coolant_material <br> \
            blanket_structural_material <br> \
            blanket_breeder_material <br> \
            blanket_multiplier_material <br> \
            blanket_coolant_material <br> \
            blanket_breeder_li6_enrichment_fraction <br> \
            blanket_breeder_packing_fraction <br> \
            blanket_multiplier_packing_fraction <br> \
            selected_blanket_fractions <br> \
            <br> \
            <br> \
            <br> \
            URL endpoint with optional arguments <br> \
            /find_tbr_model_sphere_with_no_firstwall <br> \
            blanket_structural_material <br> \
            blanket_breeder_material <br> \
            blanket_multiplier_material <br> \
            blanket_coolant_material <br> \
            blanket_breeder_li6_enrichment_fraction <br> \
            blanket_breeder_packing_fraction <br> \
            blanket_multiplier_packing_fraction <br> \
            selected_blanket_fractions <br> \
            <br> \
            <br> \
            <br> \
            Arguments take the form ... <br> \
            http://localhost:8080/find_tbr_model_sphere_with_firstwall?=firstwall_thickness=20 <br> \
            http://localhost:8080/find_tbr_model_sphere_with_firstwall?=firstwall_thickness=20&blanket_breeder_material=Li4SiO4 <br> \
            <br> \
            <br> \
            <br> \
            Argument options are <br> \
            firstwall_thickness 0 to 20 <br> \
            firstwall_amour_material '+str(firstwall_amour_material_options)+'<br> \
            firstwall_structural_material '+str(firstwall_structural_material_options)+'<br> \
            firstwall_coolant_material '+str(firstwall_coolant_material_options)+'<br> \
            blanket_structural_material '+str(blanket_structural_material_options)+'<br> \
            blanket_breeder_material '+str(blanket_breeder_material_options)+'<br> \
            blanket_multiplier_material '+str(blanket_multiplier_material_options)+'<br> \
            blanket_coolant_material '+str(blanket_coolant_material_options)+'<br> \
            blanket_breeder_li6_enrichment_fraction 0 to 1 <br> \
            blanket_breeder_packing_fraction 0 to 1 <br> \
            blanket_multiplier_packing_fraction 0 to 1 <br> \
            blanket_multiplier_fraction =  0 to 1 and sums to 1 with the other 3 blanket fractions <br> \
            blanket_breeder_fraction =  0 to 1 and sums to 1 with the other 3 blanket fractions <br> \
            blanket_structural_fraction =  0 to 1 and sums to 1 with the other 3 blanket fractions <br> \
            blanket_coolant_fraction = =  0 to 1 and sums to 1 with the other 3 blanket fractions <br> \
            <br> \
            '

@application.route('/' ,methods=['GET','POST'])
def return_help():
    return help_hints

@application.route('/find_tbr' ,methods=['GET','POST'])
def return_specific_help():
    return help_hints



@application.route('/find_tbr_model_sphere_with_firstwall' ,methods=['GET','POST'])
def call_find_tbr_model_sphere_with_firstwall():

    firstwall_thickness = request.args.get('firstwall_thickness', 
                                  type=float,
                                  default=random.choice(firstwall_thicknesses)
                                  )

    firstwall_amour_material = request.args.get('firstwall_amour_material', 
                                  type=str,
                                  default=random.choice(firstwall_amour_material_options)
                                  )

    firstwall_structural_material = request.args.get('firstwall_structural_material', 
                                  type=str,
                                  default=random.choice(firstwall_structural_material_options)
                                  )

    firstwall_coolant_material = request.args.get('firstwall_coolant_material', 
                                  type=str,
                                  default=random.choice(firstwall_coolant_material_options)
                                  )

    blanket_structural_material = request.args.get('blanket_structural_material', 
                                  type=str,
                                  default=random.choice(blanket_structural_material_options)
                                  )

    blanket_breeder_material = request.args.get('blanket_breeder_material', 
                                  type=str,
                                  default=random.choice(blanket_breeder_material_options)
                                  )

    blanket_multiplier_material = request.args.get('blanket_multiplier_material', 
                                  type=str,
                                  default=random.choice(blanket_multiplier_material_options)
                                  )

    blanket_coolant_material = request.args.get('blanket_coolant_material', 
                                  type=str,
                                  default=random.choice(blanket_coolant_material_options)
                                  )

    blanket_breeder_li6_enrichment_fraction = request.args.get('blanket_breeder_li6_enrichment_fraction', 
                                  type=float,
                                  default=random.choice(blanket_breeder_li6_enrichment_fractions)
                                  )

    blanket_breeder_packing_fraction = request.args.get('blanket_breeder_packing_fraction', 
                                  type=float,
                                  default=random.choice(blanket_breeder_packing_fractions)
                                  )

    blanket_multiplier_packing_fraction = request.args.get('blanket_multiplier_packing_fraction', 
                                  type=float,
                                  default=random.choice(blanket_multiplier_packing_fractions)
                                  )

    # selected_blanket_fractions = request.args.get('selected_blanket_fractions', 
    #                               type=list,
    #                               default=random.choice(blanket_fractions)
    #                               )   
    
    selected_blanket_fractions = random.choice(blanket_fractions)

    blanket_multiplier_fraction = request.args.get('blanket_multiplier_fraction', 
                                  type=float,
                                  default=selected_blanket_fractions[0]
                                  )  

    blanket_breeder_fraction = request.args.get('blanket_breeder_fraction', 
                                  type=float,
                                  default=selected_blanket_fractions[1]
                                  )  

    blanket_structural_fraction = request.args.get('blanket_structural_fraction', 
                                  type=float,
                                  default=selected_blanket_fractions[2]
                                  )  

    blanket_coolant_fraction = request.args.get('blanket_coolant_fraction', 
                                  type=float,
                                  default=selected_blanket_fractions[3]
                                  )  



    inputs_and_results = find_tbr_model_sphere_with_firstwall(
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




@application.route('/find_tbr_model_sphere_with_no_firstwall' ,methods=['GET','POST'])
def call_find_tbr_model_sphere_with_no_firstwall():

    blanket_structural_material = request.args.get('blanket_structural_material', 
                                  type=str,
                                  default=random.choice(blanket_structural_material_options)
                                  )

    blanket_breeder_material = request.args.get('blanket_breeder_material', 
                                  type=str,
                                  default=random.choice(blanket_breeder_material_options)
                                  )

    blanket_multiplier_material = request.args.get('blanket_multiplier_material', 
                                  type=str,
                                  default=random.choice(blanket_multiplier_material_options)
                                  )

    blanket_coolant_material = request.args.get('blanket_coolant_material', 
                                  type=str,
                                  default=random.choice(blanket_coolant_material_options)
                                  )

    blanket_breeder_li6_enrichment_fraction = request.args.get('blanket_breeder_li6_enrichment_fraction', 
                                  type=float,
                                  default=random.choice(blanket_breeder_li6_enrichment_fractions)
                                  )

    blanket_breeder_packing_fraction = request.args.get('blanket_breeder_packing_fraction', 
                                  type=float,
                                  default=random.choice(blanket_breeder_packing_fractions)
                                  )

    blanket_multiplier_packing_fraction = request.args.get('blanket_multiplier_packing_fraction', 
                                  type=float,
                                  default=random.choice(blanket_multiplier_packing_fractions)
                                  )

    selected_blanket_fractions = random.choice(blanket_fractions)

    blanket_multiplier_fraction = request.args.get('blanket_multiplier_fraction', 
                                  type=float,
                                  default=selected_blanket_fractions[0]
                                  )  

    blanket_breeder_fraction = request.args.get('blanket_breeder_fraction', 
                                  type=float,
                                  default=selected_blanket_fractions[1]
                                  )  

    blanket_structural_fraction = request.args.get('blanket_structural_fraction', 
                                  type=float,
                                  default=selected_blanket_fractions[2]
                                  )  

    blanket_coolant_fraction = request.args.get('blanket_coolant_fraction', 
                                  type=float,
                                  default=selected_blanket_fractions[3]
                                  )  

    inputs_and_results = find_tbr_model_sphere_with_no_firstwall(
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