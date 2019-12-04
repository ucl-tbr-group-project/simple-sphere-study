" The aim of this plot is to show max tbr values from 4 different scenarios"
" a slider bar can be used to move between scenarios "
" https://community.plot.ly/t/multiple-traces-with-a-single-slider-in-plotly/16356/2 "
" max tbr with no li6 enrichment, no multiplier"
" max tbr with li6 enrichment, no multiplier"
" max tbr with li6 enrichment, with multiplier"
" max tbr with no li6 enrichment with multiplier"
" max tbr from graded blanekts"


import plotly.graph_objects as go
import pandas as pd

data = pd.read_json('results_new.json') 

x = ['Product A', 'Product B', 'Product C']
y = [20, 14, 23]

fig = go.Figure()

blanket_breeder_materials = data['blanket_breeder_material'].unique()

print(blanket_breeder_materials)
max_tbr_values = []

for blanket_breeder_material in blanket_breeder_materials:
    filtered_data = data[data.blanket_breeder_material == blanket_breeder_material]

    max_tbr_values.append(max(filtered_data.tbr))

fig = fig.add_trace(go.Scatter(
                        y=max_tbr_values,
                        x=blanket_breeder_materials, 
                        text=max_tbr_values,
                        mode='markers',
                        marker=dict(size=20)
                    )
                    )

#TODO set the Y axis to start at 0
fig.update_layout(
                  yaxis_title="TBR",
                  xaxis_title="Breeder material",
                 )  

fig.show()

# filtered_data_yes_enrichment_no_multiplier
# filtered_data_yes_enrichment__multiplier