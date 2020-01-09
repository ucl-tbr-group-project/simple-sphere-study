import numpy as np
import json
from tqdm import tqdm
from tbr_utils import find_tbr

import openmc
import random


firstwall_coolant_material_options = ['no firstwall','H2O', 'He', 'D2O']
blanket_coolant_material_options = ['H2O', 'He', 'D2O']
blanket_multiplier_material_options = ['Be', 'Be12Ti']
blanket_breeder_material_options = ['Li4SiO4','Li2TiO3']
blanket_structural_material_options = ['SiC','eurofer']
firstwall_amour_material_options = ['tungsten']
firstwall_structural_material_options = ['SiC','eurofer']
firstwall_amour_fraction = 0.055262
firstwall_structural_fraction = 0.253962
firstwall_coolant_fraction = 0.690776
# [0.055262, 0.253962, 0.690776] #based on HCPB paper with 2mm W firstwall

blanket_breeder_li6_enrichment_fractions = np.linspace(start=0., stop=1., num=10, endpoint=True).tolist()
blanket_breeder_li6_enrichment_fractions.append(0.0759)
blanket_breeder_packing_fractions = np.linspace(start=0.6, stop=1., num=10, endpoint=True).tolist()
blanket_multiplier_packing_fractions = np.linspace(start=0.6, stop=1., num=10, endpoint=True).tolist()

blanket_structural_fractions = []
blanket_multiplier_fractions = []
blanket_breeder_fractions = []
blanket_coolant_fractions = []

for i in range(50):
    blanket_fractions = np.random.dirichlet(np.ones(4),size=1)


def random_simulation():

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

    inputs_and_results = find_tbr( 
                                    firstwall_amour_material,
                                    firstwall_amour_fraction,

                                    firstwall_structural_material,
                                    firstwall_structural_fraction,

                                    firstwall_coolant_material,
                                    firstwall_coolant_fraction,

                                    blanket_structural_material, 
                                    blanket_structural_fraction,
                                    
                                    blanket_coolant_material, 
                                    blanket_coolant_fraction,

                                    blanket_multiplier_fraction,
                                    blanket_multiplier_material,

                                    blanket_breeder_fraction,
                                    blanket_breeder_material,

                                    blanket_breeder_li6_enrichment_fraction,
                                    blanket_breeder_packing_fraction,
                                    blanket_multiplier_packing_fraction
                                    )

    return inputs_and_results
    print('done')

results = []
for x in range(500):
    result = random_simulation()
    results.append(result)
    with open('results_grid3.json', 'w') as fp:
        json.dump(results, fp, indent = 4)    
