
from material_maker_functions import Material, MultiMaterial
import json
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
import openmc
from skopt import gp_minimize, dump, load
from tbr_utils import *


if __name__ == "__main__":


    firstwall_options = [(['no firstwall']),(['He']),(['H2O'])]
    blanket_multiplier_materials_options = [(['Be']),(['Be12Ti'])]
    blanket_breeder_materials_options = [(['Li4SiO4']),(['Li2TiO3'])]
    blanket_breeder_li6_enrichment_options = [(0., 1.0),([0.0759])]
    breeder_to_breeder_plus_multiplier_options = [(0., 1.0),([1])]
    blanket_steel_options = [([0.]),([0.1]),([0.2]),([0.3]),([0.4]),([0.5])]

    all_iterations = []

    for firstwall_option, blanket_multiplier_materials_option, blanket_breeder_materials_option, blanket_breeder_li6_enrichment_option, breeder_to_breeder_plus_multiplier_option, blanket_steel_option in zip(firstwall_options, blanket_multiplier_materials_options, blanket_breeder_materials_options, blanket_breeder_li6_enrichment_options, breeder_to_breeder_plus_multiplier_options, blanket_steel_options):


        res = gp_minimize(find_graded_tbr_optimisation, 
                        [
                        (0., 1.0), # layer 1 thickness_fraction
                        (0., 1.0), # layer 2 thickness_fraction
                        (0., 1.0), # layer 2 layer_li6_enrichments
                        (0., 1.0), # layer 2 layer_li6_enrichments
                        (0., 1.0), # layer 1 layer_fraction_of_breeder_in_breeder_plus_multiplier_volume
                        (0., 1.0), # layer 2 layer_fraction_of_breeder_in_breeder_plus_multiplier_volume
                        blanket_multiplier_materials_option, # blanket_multiplier_material
                        blanket_breeder_materials_options, # blanket_breeder_material
                        firstwall_options, # firstwall_coolant
                        blanket_steel_options, # blanket_steel_fraction
                        ],
                        n_calls = 20)

        iteration = convert_res_to_json_layered(input_res = res)
        all_iterations = all_iterations + iteration

        res = gp_minimize(find_graded_tbr_optimisation, 
                        [
                        (0., 1.0), # layer 1 thickness_fraction
                        (0., 1.0), # layer 2 thickness_fraction
                        (0., 1.0), # layer 3 thickness_fraction
                        (0., 1.0), # layer 1 layer_li6_enrichments
                        (0., 1.0), # layer 2 layer_li6_enrichments
                        (0., 1.0), # layer 3 layer_li6_enrichments
                        (0., 1.0), # layer 1 layer_fraction_of_breeder_in_breeder_plus_multiplier_volume
                        (0., 1.0), # layer 2 layer_fraction_of_breeder_in_breeder_plus_multiplier_volume
                        (0., 1.0), # layer 3 layer_fraction_of_breeder_in_breeder_plus_multiplier_volume
                        blanket_multiplier_materials_option, # blanket_multiplier_material
                        blanket_breeder_materials_options, # blanket_breeder_material
                        firstwall_options, # firstwall_coolant
                        blanket_steel_options, # blanket_steel_fraction
                        ],
                        n_calls = 20)
    
        iteration = convert_res_to_json_layered(input_res = res)
        all_iterations = all_iterations + iteration



        res = gp_minimize(find_graded_tbr_optimisation, 
                        [
                        (0., 1.0), # layer 1 thickness_fraction
                        (0., 1.0), # layer 2 thickness_fraction
                        (0., 1.0), # layer 3 thickness_fraction
                        (0., 1.0), # layer 4 thickness_fraction
                        (0., 1.0), # layer 1 layer_li6_enrichments
                        (0., 1.0), # layer 2 layer_li6_enrichments
                        (0., 1.0), # layer 3 layer_li6_enrichments
                        (0., 1.0), # layer 4 layer_li6_enrichments
                        (0., 1.0), # layer 1 layer_fraction_of_breeder_in_breeder_plus_multiplier_volume
                        (0., 1.0), # layer 2 layer_fraction_of_breeder_in_breeder_plus_multiplier_volume
                        (0., 1.0), # layer 3 layer_fraction_of_breeder_in_breeder_plus_multiplier_volume
                        (0., 1.0), # layer 4 layer_fraction_of_breeder_in_breeder_plus_multiplier_volume
                        blanket_multiplier_materials_option, # blanket_multiplier_material
                        blanket_breeder_materials_options, # blanket_breeder_material
                        firstwall_options, # firstwall_coolant
                        blanket_steel_options, # blanket_steel_fraction
                        ],
                        n_calls = 20)
    
        iteration = convert_res_to_json_layered(input_res = res)
        all_iterations = all_iterations + iteration



    with open('results_graded_optimisation.json', 'w') as fp:
        json.dump(all_iterations, fp, indent = 4)  

    