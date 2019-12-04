import numpy as np
import json
from tqdm import tqdm
from tbr_utils import find_tbr

firstwall_coolant_options = ['no firstwall','H2O', 'He']
blanket_multiplier_material_options = ['Be', 'Be12Ti']
blanket_breeder_material_options = ['Li4SiO4','Li2TiO3']

blanket_breeder_li6_enrichment_fractions = np.linspace(start=0., stop=1., num=10, endpoint=True).tolist()
blanket_breeder_li6_enrichment_fractions.append(0.0759)


blanket_steel_fractions = []
blanket_multiplier_fractions = []
blanket_breeder_fractions = []
for blanket_steel_fraction in [0.,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]: 

    available_space = 1. - blanket_steel_fraction
    for blanket_breeder_fraction, blanket_multiplier_fraction in zip(
                                                                     [0.,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
                                                                     [0.,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0][::-1]
                                                                     ):
            blanket_steel_fractions.append(blanket_steel_fraction)
            blanket_multiplier_fractions.append(blanket_multiplier_fraction*available_space)
            blanket_breeder_fractions.append(blanket_breeder_fraction*available_space)

print(len(blanket_steel_fractions))
results = []

for firstwall_coolant in tqdm(firstwall_coolant_options, desc='outer0 loop', leave=True):
    for blanket_breeder_material in tqdm(blanket_breeder_material_options, desc='inner1 loop', leave=True):
        for blanket_multiplier_material in tqdm(blanket_multiplier_material_options, desc='inner2 loop', leave=True):
            for blanket_breeder_li6_enrichment_fraction in tqdm(blanket_breeder_li6_enrichment_fractions, desc='inner3 loop', leave=True):
                for blanket_multiplier_fraction, blanket_breeder_fraction, blanket_steel_fraction in tqdm(zip(blanket_multiplier_fractions, blanket_breeder_fractions, blanket_steel_fractions), leave=True):
                    result = {}
                    tbr = find_tbr(firstwall_coolant=firstwall_coolant, 
                                            blanket_steel_fraction=blanket_steel_fraction, 
                                            blanket_multiplier_fraction=blanket_multiplier_fraction,
                                            blanket_multiplier_material=blanket_multiplier_material,
                                            blanket_breeder_fraction=blanket_breeder_fraction,
                                            blanket_breeder_material=blanket_breeder_material,
                                            blanket_breeder_li6_enrichment_fraction=blanket_breeder_li6_enrichment_fraction
                                            )
                    result['tbr'] = tbr
                    # result['tbr_std_dev'] = tally_std_dev
                    result['firstwall_coolant'] = firstwall_coolant 
                    result['blanket_steel_fraction'] = blanket_steel_fraction 
                    result['blanket_multiplier_fraction'] = blanket_multiplier_fraction
                    result['blanket_multiplier_material'] = blanket_multiplier_material
                    result['blanket_breeder_fraction'] = blanket_breeder_fraction
                    result['blanket_breeder_material'] = blanket_breeder_material
                    result['blanket_breeder_li6_enrichment_fraction'] = blanket_breeder_li6_enrichment_fraction
                    with open('results_grid.json', 'w') as fp:
                        json.dump(results, fp, indent = 4)    



