
from skopt import gp_minimize, dump, load
from tbr_utils import *
import json

if __name__ == "__main__":

    iter_limit = 11

    firstwall_options = [(['no firstwall']),(['He']),(['H2O'])]
    blanket_multiplier_materials_options = [(['Be']),(['Be12Ti'])]
    blanket_breeder_materials_options = [(['Li4SiO4']),(['Li2TiO3'])]
    blanket_breeder_li6_enrichment_options = [(0., 1.0),([0.0759])]
    breeder_to_breeder_plus_multiplier_options = [(0., 1.0),([1])]
    blanket_steel_options = [([0.]),([0.1]),([0.2]),([0.3]),([0.4]),([0.5])]
# inputs ['He'] ['Be12Ti'] ['Li2TiO3'] [0.0759] [1] [0.1] try changing to 0.10001
    all_iterations = []

    for firstwall_option, blanket_multiplier_materials_option, blanket_breeder_materials_option, blanket_breeder_li6_enrichment_option, breeder_to_breeder_plus_multiplier_option, blanket_steel_option in zip(firstwall_options, blanket_multiplier_materials_options, blanket_breeder_materials_options, blanket_breeder_li6_enrichment_options, breeder_to_breeder_plus_multiplier_options, blanket_steel_options):

        print('inputs',firstwall_option, blanket_multiplier_materials_option, blanket_breeder_materials_option, blanket_breeder_li6_enrichment_option, breeder_to_breeder_plus_multiplier_option, blanket_steel_option)
        try:
            res = gp_minimize(find_tbr_optimisation, [
                                                    firstwall_option,      # firstwall_coolant
                                                    blanket_steel_option,        # blanket_steel_fraction
                                                    blanket_multiplier_materials_option,      # blanket_multiplier_material
                                                    blanket_breeder_materials_option, # blanket_breeder_material
                                                    breeder_to_breeder_plus_multiplier_option,     # breeder_to_breeder_plus_multiplier_fraction
                                                    blanket_breeder_li6_enrichment_option      # blanket_breeder_li6_enrichment_fraction
                                                    ],
                                                    n_calls = iter_limit)

            iterations = convert_res_to_json(input_res = res)
            all_iterations = all_iterations+ iterations
        except:
            print('inputs failed',firstwall_option, blanket_multiplier_materials_option, blanket_breeder_materials_option, blanket_breeder_li6_enrichment_option, breeder_to_breeder_plus_multiplier_option, blanket_steel_option)
       


    with open('results_hom_optimisation.json', 'w') as fp:
        json.dump(all_iterations, fp, indent = 4)  

    