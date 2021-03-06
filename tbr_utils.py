
import json
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
import openmc
from neutronics_material_maker import Material, MultiMaterial

try:
    from skopt import load
except:
    print('scikit opt not available')

def convert_res_to_json_layered(input_res = None, input_filename = None, output_filename = None):

    if input_res == None and input_filename != None:
        res = load(filename='hom_optimisation_res')
    elif input_res != None and input_filename == None:
        res = input_res
    else:
        print('input res must be provided either as a filename of a dump or as the res object')

    results = []
    for x, output_parameter in zip(res.x_iters, res.func_vals):
        result = {}

        number_of_layers = int((len(x) - 4)/3)
        print('number_of_layers',number_of_layers)

        layer_thickness_fractions = x[:number_of_layers]
        print('layer_thickness_fractions',layer_thickness_fractions)

        layer_li6_enrichments = x[number_of_layers:number_of_layers*2]
        print('layer_li6_enrichments',layer_li6_enrichments)

        layer_fractions_of_breeder_in_breeder_plus_multiplier_volume = x[number_of_layers*2:number_of_layers*3:]
        print('layer_fractions_of_breeder_in_breeder_plus_multiplier_volume',layer_fractions_of_breeder_in_breeder_plus_multiplier_volume)

        blanket_multiplier_material = x[-4]
        print('blanket_multiplier_material',blanket_multiplier_material)

        blanket_breeder_material = x[-3]
        print('blanket_breeder_material',blanket_breeder_material)
        
        firstwall_coolant = x[-2]
        print('firstwall_coolant',firstwall_coolant)
        
        blanket_structural_fraction = x[-1]
        print('blanket_structural_fraction',blanket_structural_fraction)

        result['tbr'] = 1. / output_parameter
        result['number_of_layers'] = number_of_layers
        result['layer_thickness_fractions'] = layer_thickness_fractions
        result['layer_li6_enrichments'] = layer_li6_enrichments
        # result['layer_breeder_fractions'] = layer_breeder_fractions
        result['blanket_multiplier_material'] = blanket_multiplier_material
        result['blanket_breeder_material'] = blanket_breeder_material
        result['firstwall_coolant'] = firstwall_coolant
        result['blanket_structural_fraction'] = blanket_structural_fraction
        # result['tbr_std_dev'] = tally_std_dev 
        result['fraction_of_breeder_in_breeder_plus_multiplier_volume'] = layer_fractions_of_breeder_in_breeder_plus_multiplier_volume
        


        layer_multiplier_fractions = []
        layer_breeder_fractions = []
        for entry in layer_fractions_of_breeder_in_breeder_plus_multiplier_volume:
            layer_multiplier_fractions.append((1. - entry) * (1. - blanket_structural_fraction))
        
            layer_breeder_fractions.append(entry * (1. - blanket_structural_fraction))

        result['blanket_multiplier_fraction'] = layer_multiplier_fractions
        result['blanket_breeder_fraction'] = layer_breeder_fractions

        results.append(result)

    if output_filename != None:
        with open(output_filename, 'w') as fp:
            json.dump(results, fp, indent = 4)  
    return results

def convert_res_to_json(input_res = None, input_filename = None, output_filename = None):

    if input_res == None and input_filename != None:
        res = load(filename='hom_optimisation_res')
    elif input_res != None and input_filename == None:
        res = input_res
    else:
        print('input res must be provided either as a filename of a dump or as the res object')

    results = []
    for input_parameters, output_parameter in zip(res.x_iters, res.func_vals):
        result = {}
        result['tbr'] = 1. / output_parameter
        # result['tbr_std_dev'] = tally_std_dev
        result['firstwall_coolant'] = input_parameters[0] 
        blanket_structural_fraction = input_parameters[1]  
        result['blanket_structural_fraction'] = blanket_structural_fraction
        result['blanket_multiplier_material'] = input_parameters[2]
        result['blanket_breeder_material'] = input_parameters[3]
        result['blanket_breeder_li6_enrichment_fraction'] = input_parameters[4]
        
        breeder_to_breeder_plus_multiplier_fraction = input_parameters[5]
        result['fraction_of_breeder_in_breeder_plus_multiplier_volume'] = breeder_to_breeder_plus_multiplier_fraction
        
        result['blanket_multiplier_fraction'] = (1. - breeder_to_breeder_plus_multiplier_fraction) * (1. - blanket_structural_fraction)
        result['blanket_breeder_fraction'] = breeder_to_breeder_plus_multiplier_fraction * (1. - blanket_structural_fraction)
        results.append(result)

    if output_filename != None:
        with open(output_filename, 'w') as fp:
            json.dump(results, fp, indent = 4)  
    return results

def find_tbr_optimisation(x):
    firstwall_coolant = x[0]
    blanket_structural_fraction = x[1]
    blanket_multiplier_material = x[2]
    blanket_breeder_material = x[3]
    blanket_breeder_li6_enrichment_fraction = x[4]
    breeder_to_breeder_plus_multiplier_fraction = x[5]

    blanket_multiplier_fraction = (1. - breeder_to_breeder_plus_multiplier_fraction) * (1. - blanket_structural_fraction) 
    blanket_breeder_fraction = breeder_to_breeder_plus_multiplier_fraction * (1. - blanket_structural_fraction)

    tbr = find_tbr(firstwall_coolant, 
                    blanket_structural_fraction, 
                    blanket_multiplier_fraction,
                    blanket_multiplier_material,
                    blanket_breeder_fraction,
                    blanket_breeder_material,
                    blanket_breeder_li6_enrichment_fraction
                    )

    return 1./tbr

def find_graded_tbr_optimisation(x):
    """
    Inputs is a single list of: 
        layer_thickness_fractions, 
        layer_li6_enrichment_fractions, 
        layer_breeder_fractions
    Output is Tritium breeding Ration (TBR)
    """
    print('varibles being used',x)
    number_of_layers = int((len(x) - 4)/3)
    print('number_of_layers',number_of_layers)

    layer_thickness_fractions = x[:number_of_layers]
    print('layer_thickness_fractions',layer_thickness_fractions)

    layer_li6_enrichments = x[number_of_layers:number_of_layers*2]
    print('layer_li6_enrichments',layer_li6_enrichments)

    layer_fractions_of_breeder_in_breeder_plus_multiplier_volume = x[number_of_layers*2:number_of_layers*3:]
    print('layer_fractions_of_breeder_in_breeder_plus_multiplier_volume',layer_fractions_of_breeder_in_breeder_plus_multiplier_volume)

    blanket_multiplier_material = x[-4]
    print('blanket_multiplier_material',blanket_multiplier_material)

    blanket_breeder_material = x[-3]
    print('blanket_breeder_material',blanket_breeder_material)
    
    firstwall_coolant = x[-2]
    print('firstwall_coolant',firstwall_coolant)
    
    blanket_structural_fraction = x[-1]
    print('blanket_structural_fraction',blanket_structural_fraction)

    layer_multiplier_fractions = []
    layer_breeder_fractions = []
    for entry in layer_fractions_of_breeder_in_breeder_plus_multiplier_volume:
        layer_multiplier_fractions.append((1. - entry) * (1. - blanket_structural_fraction))
    
        layer_breeder_fractions.append(entry * (1. - blanket_structural_fraction))

    thickness = 200 #2m
    inner_radius = 1000 #10m
    firstwall_thickness = 2.5 #2.5cm from hcpb fusion paper

    tbr = find_tbr_from_graded_blanket(number_of_layers,
                                       layer_thickness_fractions,
                                       layer_li6_enrichments,
                                       layer_breeder_fractions,
                                       layer_multiplier_fractions,
                                       blanket_multiplier_material,
                                       blanket_breeder_material,
                                       firstwall_coolant,
                                       blanket_structural_fraction,
                                       inner_radius,
                                       thickness,
                                       firstwall_thickness)
    return 1. / tbr

def find_tbr_from_graded_blanket(number_of_layers,
                                layer_thickness_fractions,
                                layer_li6_enrichments,
                                layer_breeder_fractions,
                                layer_multiplier_fractions,
                                blanket_structural_material,
                                blanket_multiplier_material,
                                blanket_breeder_material,
                                firstwall_coolant,
                                blanket_structural_fraction,
                                inner_radius,
                                thickness,
                                firstwall_thickness
                                ):

    batches = 10

    thickness_fraction_scaler = thickness / sum(layer_thickness_fractions)
    print('thickness_fraction_scaler',thickness_fraction_scaler)


    if firstwall_coolant == 'no firstwall':
        
        breeder_blanket_inner_surface = openmc.Sphere(r=inner_radius)
        inner_void_region = -breeder_blanket_inner_surface 
        inner_void_cell = openmc.Cell(region=inner_void_region) 
        inner_void_cell.name = 'inner_void'
        surfaces = [breeder_blanket_inner_surface]

        additional_thickness = 0
        all_layers_materials = []
        all_cells = [inner_void_cell]
        for i, (layer_thickness, layer_enrichment, layer_breeder_fraction, layer_multiplier_fraction) in enumerate(zip(
                                            layer_thickness_fractions,
                                            layer_li6_enrichments,
                                            layer_breeder_fractions,
                                            layer_multiplier_fractions
                                    )):
            print(i, layer_thickness, layer_enrichment, layer_breeder_fraction)
            
            layer_material = MultiMaterial(material_name = 'layer_'+str(i)+'_material',
                                                materials = [
                                                            Material(blanket_breeder_material, 
                                                                        enrichment_fraction=layer_enrichment),
                                                            Material(blanket_multiplier_material),
                                                            Material(blanket_structural_material)
                                                            ],
                                                fracs = [layer_breeder_fraction, layer_multiplier_fraction, blanket_structural_fraction]
                                                ).neutronics_material
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
    else:
        #firstwall is present

        firstwall_material = MultiMaterial(material_name = 'firstwall_material',
                                materials = [
                                            Material('tungsten'),
                                            Material(firstwall_coolant),
                                            Material(blanket_structural_material)
                                            ],
                                fracs = [0.055262, 0.253962, 0.690776] #based on HCPB paper with 2mm W firstwall
                                ).neutronics_material


        breeder_blanket_inner_surface = openmc.Sphere(r=inner_radius+firstwall_thickness)
        firstwall_outer_surface = openmc.Sphere(r=inner_radius) 
        surfaces = [firstwall_outer_surface, breeder_blanket_inner_surface]

        inner_void_region = -firstwall_outer_surface 
        inner_void_cell = openmc.Cell(region=inner_void_region) 
        inner_void_cell.name = 'inner_void'

        firstwall_region = +firstwall_outer_surface & -breeder_blanket_inner_surface 
        firstwall_cell = openmc.Cell(region=firstwall_region)
        firstwall_cell.fill = firstwall_material
        firstwall_cell.name = 'firstwall'

        additional_thickness = 0
        all_layers_materials = [firstwall_material]
        all_cells = [inner_void_cell,firstwall_cell]

        for i, (layer_thickness, layer_enrichment, layer_breeder_fraction, layer_multiplier_fraction) in enumerate(zip(
                                            layer_thickness_fractions,
                                            layer_li6_enrichments,
                                            layer_breeder_fractions,
                                            layer_multiplier_fractions
                                    )):
            print(i, layer_thickness, layer_enrichment, layer_breeder_fraction)
            
            layer_material = MultiMaterial('layer_'+str(i)+'_material',
                                                materials = [
                                                            Material(blanket_breeder_material, 
                                                                        enrichment_fraction=layer_enrichment),
                                                            Material(blanket_multiplier_material),
                                                            Material(blanket_structural_material)
                                                            ],
                                                volume_fractions = [layer_breeder_fraction, layer_multiplier_fraction, blanket_structural_fraction]
                                                )
            all_layers_materials.append(layer_material)

            additional_thickness = additional_thickness + (layer_thickness * thickness_fraction_scaler)
            print('additional_thickness',additional_thickness)

            if i == number_of_layers-1:
                layer_outer_surface = openmc.Sphere(r=inner_radius+firstwall_thickness+additional_thickness, boundary_type='vacuum')
            else:    
                layer_outer_surface = openmc.Sphere(r=inner_radius+firstwall_thickness+additional_thickness)
            
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
    tally.scores = ['(n,Xt)'] #could be (n,Xt)
    tallies.append(tally)

    model = openmc.model.Model(geom, mats, sett, tallies)
    model.export_to_xml()
    # model.run()
    openmc.lib.run()


    sp = openmc.StatePoint('statepoint.'+str(batches)+'.h5')

    tally = sp.get_tally(name='TBR')

    df = tally.get_pandas_dataframe()

    return df['mean'].sum()

def make_blanket_material(  blanket_structural_material, 
                            blanket_structural_fraction,

                            blanket_coolant_material, 
                            blanket_coolant_fraction,

                            blanket_multiplier_material,
                            blanket_multiplier_fraction,

                            blanket_breeder_material,
                            blanket_breeder_fraction,

                            blanket_breeder_li6_enrichment_fraction,
                            blanket_breeder_packing_fraction,
                            blanket_multiplier_packing_fraction
                            ):

    if blanket_coolant_material == 'He':
        temperature_in_C=400
        pressure_in_Pa=8e6
    elif blanket_coolant_material in ['H2O','D2O']:
        temperature_in_C=305
        pressure_in_Pa=15.5e6


    blanket_material =  MultiMaterial(material_name = 'blanket_material',
                        materials = [
                                     Material(material_name = blanket_structural_material),
                                     Material(material_name = blanket_coolant_material,
                                              temperature_in_C = temperature_in_C,
                                              pressure_in_Pa = pressure_in_Pa),
                                     Material(material_name = blanket_multiplier_material,
                                              packing_fraction = blanket_multiplier_packing_fraction),
                                     Material(material_name = blanket_breeder_material, 
                                              enrichment_fraction=blanket_breeder_li6_enrichment_fraction,
                                              temperature_in_C = 500,
                                              packing_fraction = blanket_breeder_packing_fraction),
                                    ],
                        fracs = [blanket_structural_fraction,
                                 blanket_coolant_fraction,
                                 blanket_multiplier_fraction,
                                 blanket_breeder_fraction],
                        percent_type='vo'
                        ).neutronics_material

    return blanket_material

def make_firstwall_material(
             firstwall_armour_material,
             firstwall_armour_fraction,

             firstwall_coolant_material,
             firstwall_coolant_fraction,

             firstwall_structural_material,
             firstwall_structural_fraction
             ):

    if firstwall_coolant_material == 'He':
        temperature_in_C=400
        pressure_in_Pa=8e6
    elif firstwall_coolant_material in ['H2O','D2O']:
        temperature_in_C=305
        pressure_in_Pa=15.5e6

    firstwall_material = MultiMaterial(material_name = 'firstwall_material',
                                        materials = [
                                            Material(material_name = firstwall_armour_material),
                                            Material(material_name = firstwall_coolant_material,
                                                        temperature_in_C = temperature_in_C,
                                                        pressure_in_Pa = pressure_in_Pa),
                                            Material(material_name = firstwall_structural_material)
                                        ],
                                        fracs = [firstwall_armour_fraction, 
                                                 firstwall_coolant_fraction, 
                                                 firstwall_structural_fraction
                                                            ]
                                        ).neutronics_material

    return firstwall_material

def find_tbr_model_sphere_with_no_firstwall(blanket_thickness, blanket_material, number_of_batches, particles_per_batch):

            inner_radius = 1000  #10m
            thickness = blanket_thickness
            # batches = number_of_batches

            mats = openmc.Materials([blanket_material])

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

            geom = openmc.Geometry(universe)

            #SIMULATION SETTINGS#

            sett = openmc.Settings()
            # batches = 10 # this is parsed as an argument
            sett.batches = number_of_batches
            sett.inactive = 0
            sett.particles = particles_per_batch
            sett.run_mode = 'fixed source'
            # sett.verbosity = 1

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
            tally.scores = ['(n,Xt)'] # MT 205 is the (n,Xt) reaction where X is a wildcard, if MT 105 or (n,t) then some tritium production will be missed, for example (n,nt) which happens in Li7 would be missed
            tallies.append(tally)

            model = openmc.model.Model(geom, mats, sett, tallies)
            model.export_to_xml()
            model.run()
            # openmc.lib.run()

            sp = openmc.StatePoint('statepoint.'+str(number_of_batches)+'.h5')

            tally = sp.get_tally(name='TBR')

            df = tally.get_pandas_dataframe()
            # print(df)
            tally_result = df['mean'].sum()
            tally_std_dev = df['std. dev.'].sum()

            results = {
                'tbr':tally_result,
                'tbr_error':tally_std_dev
            }

            return results

def find_tbr_model_sphere_with_firstwall(blanket_thickness, blanket_material, firstwall_material, firstwall_thickness, number_of_batches, particles_per_batch):

            inner_radius = 1000  #10m
            thickness = blanket_thickness
            # batches = number_of_batches

            mats = openmc.Materials([blanket_material, firstwall_material]) 


            breeder_blanket_inner_surface = openmc.Sphere(r=inner_radius+firstwall_thickness)
            firstwall_outer_surface = openmc.Sphere(r=inner_radius)  

            inner_void_region = -firstwall_outer_surface 
            inner_void_cell = openmc.Cell(region=inner_void_region) 
            inner_void_cell.name = 'inner_void'

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
            sett.batches = number_of_batches
            sett.inactive = 0
            sett.particles = particles_per_batch
            sett.run_mode = 'fixed source'
            # sett.verbosity = 1

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
            tally.scores = ['(n,Xt)'] # MT 205 is the (n,Xt) reaction where X is a wildcard, if MT 105 or (n,t) then some tritium production will be missed, for example (n,nt) which happens in Li7 would be missed
            tallies.append(tally)

            model = openmc.model.Model(geom, mats, sett, tallies)
            model.export_to_xml()
            model.run()
            # openmc.lib.run()

            sp = openmc.StatePoint('statepoint.'+str(number_of_batches)+'.h5')

            tally = sp.get_tally(name='TBR')

            df = tally.get_pandas_dataframe()
            # print(df)
            tally_result = df['mean'].sum()
            tally_std_dev = df['std. dev.'].sum()

            results = {
                'tbr':tally_result,
                'tbr_error':tally_std_dev
            }

            return results
