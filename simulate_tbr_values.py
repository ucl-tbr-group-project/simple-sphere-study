
from material_maker_functions import Material, MultiMaterial
import json
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
import openmc
from tqdm import tqdm


def find_tbr(firstwall_coolant, 
             blanket_steel_fraction, 
             blanket_multiplier_fraction,
             blanket_multiplier_material,
             blanket_breeder_fraction,
             blanket_breeder_material,
             blanket_breeder_li6_enrichment_fraction
             ):

            blanket_material = MultiMaterial('blanket_material',
                                                materials = [
                                                            Material(blanket_breeder_material, 
                                                                     enrichment_fraction=blanket_breeder_li6_enrichment_fraction,
                                                                     temperature_in_C = 500),
                                                            Material(blanket_multiplier_material),
                                                            Material('eurofer')
                                                            ],
                                                volume_fractions = [blanket_breeder_fraction, blanket_multiplier_fraction, blanket_steel_fraction]
                                                ).makeMaterial()
            if firstwall_coolant != 'no firstwall':
                firstwall_material = MultiMaterial('firstwall_material',
                                    materials = [
                                                Material('tungsten'),
                                                Material(firstwall_coolant),
                                                Material('eurofer')
                                                ],
                                    volume_fractions = [0.2, 0.3, 0.7]
                                    ).makeMaterial()
                                
                mats = openmc.Materials([blanket_material, firstwall_material]) 
            else:
                mats = openmc.Materials([blanket_material]) 

            inner_radius = 1000  #10m
            thickness = 200
            batches = 10
            firstwall_thickness = 2

            if firstwall_coolant == 'no firstwall':

                breeder_blanket_inner_surface = openmc.Sphere(r=inner_radius)
                inner_void_region = -breeder_blanket_inner_surface 
                inner_void_cell = openmc.Cell(region=inner_void_region) 
                inner_void_cell.name = 'inner_void'
            
                breeder_blanket_outer_surface = openmc.Sphere(r=inner_radius+thickness, boundary_type='vacuum')
                breeder_blanket_region = -breeder_blanket_outer_surface & +breeder_blanket_inner_surface
                breeder_blanket_cell = openmc.Cell(region=breeder_blanket_region) 
                breeder_blanket_cell.fill = blanket_material
                breeder_blanket_cell.name = 'breeder_blanket'

                universe = openmc.Universe(cells=[inner_void_cell, 
                                                  breeder_blanket_cell
                                                 ])
            else:

                breeder_blanket_inner_surface = openmc.Sphere(r=inner_radius+firstwall_thickness)
                inner_void_region = -breeder_blanket_inner_surface 
                inner_void_cell = openmc.Cell(region=inner_void_region) 
                inner_void_cell.name = 'inner_void'

                firstwall_thickness= 3.
                firstwall_outer_surface = openmc.Sphere(r=inner_radius)  
                firstwall_region = +firstwall_outer_surface & -breeder_blanket_inner_surface 
                firstwall_cell = openmc.Cell(region=firstwall_region)
                firstwall_cell.fill = firstwall_material
                firstwall_cell.name = 'firstwall'

                breeder_blanket_outer_surface = openmc.Sphere(r=inner_radius+firstwall_thickness+thickness, boundary_type='vacuum')
                breeder_blanket_region = -breeder_blanket_outer_surface & +breeder_blanket_inner_surface
                breeder_blanket_cell = openmc.Cell(region=breeder_blanket_region) 
                breeder_blanket_cell.fill = blanket_material
                breeder_blanket_cell.name = 'breeder_blanket'
                
                universe = openmc.Universe(cells=[inner_void_cell, 
                                                  firstwall_cell,
                                                  breeder_blanket_cell
                                                 ])

            geom = openmc.Geometry(universe)

            #SIMULATION SETTINGS#

            sett = openmc.Settings()
            # batches = 10 # this is parsed as an argument
            sett.batches = batches
            sett.inactive = 0
            sett.particles = 10000
            sett.run_mode = 'fixed source'

            source = openmc.Source()
            source.space = openmc.stats.Point((0,0,0))
            source.angle = openmc.stats.Isotropic()
            source.energy = openmc.stats.Muir(e0=14080000.0, m_rat=5.0, kt=20000.0) #neutron energy = 14.08MeV, AMU for D + T = 5, temperature is 20KeV
            # source.energy = openmc.stats.Discrete([14e6], [1])
            sett.source = source

            #TALLIES#

            tallies = openmc.Tallies()

            # define filters
            cell_filter_breeder = openmc.CellFilter(breeder_blanket_cell)
            particle_filter = openmc.ParticleFilter(['neutron']) #1 is neutron, 2 is photon
            
            tally = openmc.Tally(name='TBR')
            tally.filters = [cell_filter_breeder, particle_filter]
            tally.scores = ['205'] # MT 205 is the (n,XT) reaction where X is a wildcard, if MT 105 or (n,t) then some tritium production will be missed, for example (n,nt) which happens in Li7 would be missed
            tallies.append(tally)

            model = openmc.model.Model(geom, mats, sett, tallies)
            model.export_to_xml()
            model.run()

            sp = openmc.StatePoint('statepoint.'+str(batches)+'.h5')

            tally = sp.get_tally(name='TBR')

            df = tally.get_pandas_dataframe()
            print(df)
            tally_result = df['mean'].sum()
            tally_std_dev = df['std. dev.'].sum()

            result = {}
            result['tbr'] = tally_result
            result['tbr_std_dev'] = tally_std_dev
            result['firstwall_coolant'] = firstwall_coolant 
            result['blanket_steel_fraction'] = blanket_steel_fraction 
            result['blanket_multiplier_fraction'] = blanket_multiplier_fraction
            result['blanket_multiplier_material'] = blanket_multiplier_material
            result['blanket_breeder_fraction'] = blanket_breeder_fraction
            result['blanket_breeder_material'] = blanket_breeder_material
            result['blanket_breeder_li6_enrichment_fraction'] = blanket_breeder_li6_enrichment_fraction
            return result


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
                    results.append(find_tbr(firstwall_coolant=firstwall_coolant, 
                                            blanket_steel_fraction=blanket_steel_fraction, 
                                            blanket_multiplier_fraction=blanket_multiplier_fraction,
                                            blanket_multiplier_material=blanket_multiplier_material,
                                            blanket_breeder_fraction=blanket_breeder_fraction,
                                            blanket_breeder_material=blanket_breeder_material,
                                            blanket_breeder_li6_enrichment_fraction=blanket_breeder_li6_enrichment_fraction
                                            ))
                    with open('results_new.json', 'w') as fp:
                        json.dump(results, fp, indent = 4)    



