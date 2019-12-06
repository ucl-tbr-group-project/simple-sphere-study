import numpy as np
import json
from tqdm import tqdm
from tbr_utils import find_tbr

import openmc
import openmc.lib

# openmc.lib.init()
# mat = openmc.lib.Material(40000)

# all_stable_isotope_list = ['Ag107', 'Ag109', 'Al27', 'Ar36', 'Ar38', 'Ar40', 'As75', 'Au197', 'B10', 'B11', 'Ba130', 'Ba132', 'Ba134', 'Ba135', 'Ba136', 'Ba137', 'Ba138', 'Be9', 'Bi209','Br79', 'Br81', 'C12', 'C13', 'Ca40', 'Ca42', 'Ca43', 'Ca44', 'Ca46', 'Ca48', 'Cd106', 'Cd108', 'Cd110', 'Cd111', 'Cd112', 'Cd113', 'Cd114', 'Cd116', 'Ce136', 'Ce138', 'Ce140', 'Ce142', 'Cl35', 'Cl37', 'Co59', 'Cr50', 'Cr52', 'Cr53', 'Cr54', 'Cs133', 'Cu63', 'Cu65', 'Dy156', 'Dy158', 'Dy160', 'Dy161', 'Dy162', 'Dy163', 'Dy164', 'Er162', 'Er164', 'Er166', 'Er167', 'Er168', 'Er170', 'Eu151', 'Eu153', 'F19', 'Fe54', 'Fe56', 'Fe57', 'Fe58', 'Ga69', 'Ga71', 'Gd152', 'Gd154', 'Gd155', 'Gd156', 'Gd157', 'Gd158', 'Gd160', 'Ge70', 'Ge72', 'Ge73', 'Ge74', 'Ge76', 'H1', 'H2', 'He3', 'He4', 'Hf174', 'Hf176', 'Hf177', 'Hf178', 'Hf179', 'Hf180', 'Hg196', 'Hg198', 'Hg199', 'Hg200', 'Hg201', 'Hg202', 'Hg204', 'Ho165', 'I127', 'In113', 'In115', 'Ir191', 'Ir193', 'K39', 'K40', 'K41', 'Kr78', 'Kr80', 'Kr82', 'Kr83', 'Kr84', 'Kr86', 'La138', 'La139', 'Li6', 'Li7', 'Lu175', 'Lu176', 'Mg24', 'Mg25', 'Mg26', 'Mn55', 'Mo100', 'Mo92', 'Mo94', 'Mo95', 'Mo96', 'Mo97', 'Mo98', 'N14', 'N15', 'Na23', 'Nb93', 'Nd142', 'Nd143', 'Nd144', 'Nd145', 'Nd146', 'Nd148', 'Nd150', 'Ne20', 'Ne21', 'Ne22', 'Ni58', 'Ni60', 'Ni61', 'Ni62', 'Ni64', 'O16', 'O17', 'O18', 'Os184', 'Os186', 'Os187', 'Os188', 'Os189', 'Os190', 'Os192', 'P31', 'Pa231', 'Pb204', 'Pb206', 'Pb207', 'Pb208', 'Pd102', 'Pd104', 'Pd105', 'Pd106', 'Pd108', 'Pd110', 'Pr141', 'Pt190', 'Pt192', 'Pt194', 'Pt195', 'Pt196', 'Pt198', 'Rb85', 'Rb87', 'Re185', 'Re187', 'Rh103', 'Ru100', 'Ru101', 'Ru102', 'Ru104', 'Ru96', 'Ru98', 'Ru99', 'S32', 'S33', 'S34', 'S36', 'Sb121', 'Sb123', 'Sc45', 'Se74', 'Se76', 'Se77', 'Se78', 'Se80', 'Se82', 'Si28', 'Si29', 'Si30', 'Sm144', 'Sm147', 'Sm148', 'Sm149', 'Sm150', 'Sm152', 'Sm154', 'Sn112', 'Sn114', 'Sn115', 'Sn116', 'Sn117', 'Sn118', 'Sn119', 'Sn120', 'Sn122', 'Sn124', 'Sr84', 'Sr86', 'Sr87', 'Sr88', 'Ta180', 'Ta181', 'Tb159', 'Te120', 'Te122', 'Te123', 'Te124', 'Te125', 'Te126', 'Te128', 'Te130', 'Th232', 'Ti46', 'Ti47', 'Ti48', 'Ti49', 'Ti50', 'Tl203', 'Tl205', 'Tm169', 'U234', 'U235', 'U238', 'V50', 'V51', 'W180', 'W182', 'W183', 'W184', 'W186', 'Xe124', 'Xe126', 'Xe128', 'Xe129', 'Xe130', 'Xe131', 'Xe132', 'Xe134', 'Xe136', 'Y89', 'Yb168', 'Yb170', 'Yb171', 'Yb172', 'Yb173', 'Yb174', 'Yb176', 'Zn64', 'Zn66', 'Zn67', 'Zn68', 'Zn70', 'Zr90', 'Zr91', 'Zr92', 'Zr94', 'Zr96']
# for isotope in all_stable_isotope_list:

#     mat.add_nuclide(isotope,0.5)

# mat.set_density(2.,'g/cm3')




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
                for blanket_multiplier_fraction, blanket_breeder_fraction, blanket_steel_fraction in tqdm(zip(blanket_multiplier_fractions, blanket_breeder_fractions, blanket_steel_fractions), desc='inner4 loop', leave=True):
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
                    results.append(result)
with open('results_grid.json', 'w') as fp:
    json.dump(results, fp, indent = 4)    

# openmc.lib.finalize()