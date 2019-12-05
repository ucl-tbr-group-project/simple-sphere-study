" The aim of this plot is to show max tbr values from 4 different scenarios"
" a slider bar can be used to move between scenarios "
" https://community.plot.ly/t/multiple-traces-with-a-single-slider-in-plotly/16356/2 "
" max tbr with no li6 enrichment, no multiplier"
" max tbr with li6 enrichment, no multiplier"
" max tbr with li6 enrichment, with multiplier"
" max tbr with no li6 enrichment with multiplier"
" max tbr from graded blanekts"


import plotly.graph_objects as go
from plotly.graph_objs import Scatter, Layout, Contour, Heatmap, Surface, Scatter3d
import pandas as pd

data = pd.read_json('results_new.json') 
# data = pd.read_json('results_hom_optimisation.json') #this should have even higher TBR values
# data = pd.read_json('results_graded_optimisation.json') #this should have the highest TBR values

blanket_breeder_materials = data['blanket_breeder_material'].unique()

scenario_1 = []
scenario_2 = []
scenario_3 = []
scenario_4 = []

for blanket_breeder_material in blanket_breeder_materials:
    
    # max tbr with no li6 enrichment, no multiplier
    filtered_data_1 = data[
                        (data.blanket_breeder_material == blanket_breeder_material) &
                        (data.blanket_breeder_li6_enrichment_fraction == 0) &
                        (data.blanket_multiplier_fraction == 0)
    ]
    scenario_1.append(['No Li6 enrichment, no multiplier', filtered_data_1, blanket_breeder_material])


    # max tbr with li6 enrichment, no multiplier
    filtered_data_2 = data[
                        (data.blanket_breeder_material == blanket_breeder_material) &
                        (data.blanket_breeder_li6_enrichment_fraction > 0) &
                        (data.blanket_multiplier_fraction == 0)
    ]
    scenario_2.append(['Li6 enrichment, no multiplier', filtered_data_2, blanket_breeder_material])
  

    # max tbr with no li6 enrichment, with multiplier
    filtered_data_3 = data[
                        (data.blanket_breeder_material == blanket_breeder_material) &
                        (data.blanket_breeder_li6_enrichment_fraction == 0) &
                        (data.blanket_multiplier_fraction > 0)
    ]
    scenario_3.append(['No Li6 enrichment, with multiplier', filtered_data_3, blanket_breeder_material])


    # max tbr with li6 enrichment, with multiplier
    filtered_data_4 = data[
                        (data.blanket_breeder_material == blanket_breeder_material) &
                        (data.blanket_breeder_li6_enrichment_fraction > 0) &
                        (data.blanket_multiplier_fraction > 0)
    ]
    scenario_4.append(['Li6 enrichment, with multiplier', filtered_data_4, blanket_breeder_material])


traces = []
for scenario in (scenario_1, scenario_2, scenario_3, scenario_4):
    traces.append(Scatter(
                    y=[max(scenario[0][1].tbr), max(scenario[1][1].tbr)],
                    x=[scenario[0][2], scenario[1][2]],
                    text=[max(scenario[0][1].tbr), max(scenario[1][1].tbr)],
                    mode='markers',
                    marker=dict(size=20),
                    name=str(scenario[0][0])
    ))


layout = Layout(xaxis={'title':'Breeder material'},
                yaxis={'title':'TBR'})

fig = go.Figure({'data':traces,
                 'layout':layout})
fig.show()