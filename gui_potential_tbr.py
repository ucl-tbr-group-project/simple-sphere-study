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

blanket_breeder_materials = data['blanket_breeder_material'].unique()

materials = []
filtered_data = []
names = []

for blanket_breeder_material in blanket_breeder_materials:
    

    # max tbr with no li6 enrichment, no multiplier
    filtered_data_1 = data[
                        (data.blanket_breeder_material == blanket_breeder_material) &
                        (data.blanket_breeder_li6_enrichment_fraction == 0) &
                        (data.blanket_multiplier_fraction == 0)
    ]
    names.append('No Li6 enrichment, no multiplier')
    filtered_data.append(filtered_data_1)
    materials.append(blanket_breeder_material)


    # max tbr with li6 enrichment, no multiplier
    filtered_data_2 = data[
                        (data.blanket_breeder_material == blanket_breeder_material) &
                        (data.blanket_breeder_li6_enrichment_fraction > 0) &
                        (data.blanket_multiplier_fraction == 0)
    ]
    names.append('Li6 enrichment, no multiplier')
    filtered_data.append(filtered_data_2)
    materials.append(blanket_breeder_material)
  

    # max tbr with no li6 enrichment, with multiplier
    filtered_data_3 = data[
                        (data.blanket_breeder_material == blanket_breeder_material) &
                        (data.blanket_breeder_li6_enrichment_fraction == 0) &
                        (data.blanket_multiplier_fraction > 0)
    ]
    names.append('No Li6 enrichment, with multiplier')
    filtered_data.append(filtered_data_3)
    materials.append(blanket_breeder_material)


    # max tbr with li6 enrichment, with multiplier
    filtered_data_4 = data[
                        (data.blanket_breeder_material == blanket_breeder_material) &
                        (data.blanket_breeder_li6_enrichment_fraction > 0) &
                        (data.blanket_multiplier_fraction > 0)
    ]
    names.append('Li6 enrichment, with multiplier')
    filtered_data.append(filtered_data_4)
    materials.append(blanket_breeder_material)


traces = []

for data, material, name in zip(filtered_data, materials, names):
    traces.append(Scatter(
                    y=[max(data.tbr)],
                    x=[material],
                    text=max(data.tbr),
                    mode='markers',
                    marker=dict(size=20),
                    name=name,
    )
    )

layout = Layout(xaxis={'title':'Breeder material'},
                yaxis={'title':'TBR'})

fig = go.Figure({'data':traces,
                 'layout':layout})
fig.show()