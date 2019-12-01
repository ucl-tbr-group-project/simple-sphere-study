
from material_maker_functions import Material, MultiMaterial
import json
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
import openmc
from skopt import gp_minimize

def find_tbr(x):
    """
    Inputs is a single list of: 
        layer_thickness_fractions, 
        layer_li6_enrichment_fractions, 
        layer_breeder_fractions
    Output is Tritium breeding Ration (TBR)
    """
    print('varibles being used',x)
    number_of_layers = int(len(x)/3)
    print('number_of_layers',number_of_layers)
    layer_thickness_fractions = x[:number_of_layers]
    layer_li6_enrichments = x[number_of_layers:number_of_layers*2]
    layer_breeder_fractions = x[number_of_layers*2:]

    
    firstwall_coolant = 'none'
    blanket_breeder_material = 'Li4SiO4'
    blanket_multiplier_material = 'Be'
    blanket_steel_fraction = 0.1

    inner_radius = 1000  #10m
    thickness = 200
    batches = 10
    
    thickness_fraction_scaler = thickness / sum(layer_thickness_fractions)
    print('thickness_fraction_scaler',thickness_fraction_scaler)

    breeder_blanket_inner_surface = openmc.Sphere(r=inner_radius)
    inner_void_region = -breeder_blanket_inner_surface 
    inner_void_cell = openmc.Cell(region=inner_void_region) 
    inner_void_cell.name = 'inner_void'

    surfaces = [breeder_blanket_inner_surface]
    if firstwall_coolant == 'none':
        
        additional_thickness = 0
        all_layers_materials = []
        all_cells = [inner_void_cell]
        for i, (layer_thickness, layer_enrichment, layer_breeder_fraction) in enumerate(zip(
                                            layer_thickness_fractions,
                                            layer_li6_enrichments,
                                            layer_breeder_fractions
                                    )):
            print(i, layer_thickness, layer_enrichment, layer_breeder_fraction)
            
            layer_multiplier_fraction = 1. - (blanket_steel_fraction + layer_breeder_fraction)
            layer_material = MultiMaterial('layer_'+str(i)+'_material',
                                                materials = [
                                                            Material(blanket_breeder_material, 
                                                                        enrichment_fraction=layer_enrichment),
                                                            Material(blanket_multiplier_material),
                                                            Material('eurofer')
                                                            ],
                                                volume_fractions = [layer_breeder_fraction, layer_multiplier_fraction, blanket_steel_fraction]
                                                ).makeMaterial()
            all_layers_materials.append(layer_material)

            additional_thickness = additional_thickness + (layer_thickness * thickness_fraction_scaler)
            print('additional_thickness',additional_thickness)

            if i == number_of_layers-1:
                layer_outer_surface = openmc.Sphere(r=inner_radius+additional_thickness, boundary_type='vacuum')
            else:    
                layer_outer_surface = openmc.Sphere(r=inner_radius+additional_thickness)
            
            layer_inner_surface = surfaces[-1]
            
            layer_region = -layer_outer_surface & +layer_inner_surface
            layer_cell = openmc.Cell(region=layer_region) 
            layer_cell.fill = layer_material
            layer_cell.name = 'layer_'+str(i)+'_cell'
            
            surfaces.append(layer_outer_surface)
            all_cells.append(layer_cell)
            

        universe = openmc.Universe(cells=all_cells)
        geom = openmc.Geometry(universe)

        mats = openmc.Materials(all_layers_materials)

    sett = openmc.Settings()
    # batches = 3 # this is parsed as an argument
    sett.batches = batches
    sett.inactive = 10
    sett.particles = 500
    sett.run_mode = 'fixed source'

    source = openmc.Source()
    source.space = openmc.stats.Point((0,0,0))
    source.angle = openmc.stats.Isotropic()
    source.energy = openmc.stats.Muir(e0=14080000.0, m_rat=5.0, kt=20000.0) #neutron energy = 14.08MeV, AMU for D + T = 5, temperature is 20KeV
    sett.source = source

    #TALLIES#

    tallies = openmc.Tallies()

    # define filters
    # cell_filter_breeder = openmc.CellFilter(breeder_blanket_cell)
    particle_filter = openmc.ParticleFilter(['neutron']) #1 is neutron, 2 is photon
    
    tally = openmc.Tally(name='TBR')
    tally.filters = [particle_filter]
    tally.scores = ['205'] #could be (n,t)
    tallies.append(tally)

    model = openmc.model.Model(geom, mats, sett, tallies)

    model.run()

    sp = openmc.StatePoint('statepoint.'+str(batches)+'.h5')

    tally = sp.get_tally(name='TBR')

    df = tally.get_pandas_dataframe()

    return 1. / df['mean'].sum()



               
tbr = find_tbr([0.1, 0.2, 0.2, 0.3, 0.4, 0.4, 0.5, 0.6, 0.6])

print(tbr)          

# res = gp_minimize(find_tbr, 
#                   [
#                    (0., 1.0),
#                    (0., 1.0),
#                    (0., 1.0),
#                    (0., 1.0),
#                    (0., 1.0),
#                    (0., 1.0)
#                   ],
#                   n_calls = 11)

# print(res)