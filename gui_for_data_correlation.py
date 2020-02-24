
import streamlit as st
import json
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
from tqdm import tqdm
import itertools

@st.cache
def load_data():
        path_to_json = "outputs"
        list_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
        resultdict = []
        for filename in tqdm(list_files):
                try:
                        with open(os.path.join(path_to_json, filename), "r") as inputjson:
                                resultdict.append(json.load(inputjson))
                except:
                        print(filename)

        results_df = pd.DataFrame(resultdict)

        results_df = results_df.drop(['tbr_error', 'number_of_batches', 'particles_per_batch'], axis=1)
        print(results_df)
        return results_df


def find_type_of_entries_in_each_field(data, models):

        all_catorgorical_key_names = {}
        all_continious_key_names = {}

        for model_name in models:
                catorgorical_key_names = []
                continious_key_names = []

                model_data = data[(data['model'] == model_name)]
                # print(model_data.keys())
                model_data = model_data.dropna(axis=1, how='all')
                # print(model_data.keys())

                catorgorical_key_names = model_data.select_dtypes(include=['object']).keys()
                continious_key_names = model_data.select_dtypes(include=['float64','int']).keys()


                all_catorgorical_key_names[model_name] = catorgorical_key_names
                all_continious_key_names[model_name] = continious_key_names

        return all_catorgorical_key_names, all_continious_key_names

def plot_graphs(data, selected_y_axis, selected_x_axis, color_by):

            max_vals = []
            fig = go.Figure()

            for material in data[color_by].unique():

                    print('adding color_by',color_by, material)


                    y_data = data[(data[color_by] == material)][selected_y_axis]
                    x_data = data[(data[color_by] == material)][selected_x_axis]

                    fig.add_trace(go.Scatter(x=x_data,
                                             y=y_data,
                                            name= material,
                                            mode='markers'
                                            )
                                    )

                    max_vals.append([material,max(y_data)])


            fig.update_layout(barmode='overlay',
                            xaxis_title=selected_x_axis.replace('_',' '),
                            yaxis_title=selected_y_axis.upper(),
                            title="Impact of "+selected_x_axis.replace('_',' ')+ " on "+ selected_y_axis,
                            showlegend=True
                            )

            fig.update_traces(opacity=0.4)

            st.write(fig)
        #     return 1.
            return max_vals







data = load_data()

models = data['model'].unique()

catorgorical_key_names, continious_key_names = find_type_of_entries_in_each_field(data, models)

st.title('TBR correlation explorer')
st.text('Filter a dataset of '+str(len(data))+ ' simulations')

selected_model = st.selectbox(label = 'model', options=models )

print('selected_model',selected_model)

filtered_data = data[(data['model'] == selected_model)]

selected_x_axis = st.selectbox(label = 'x axis', options=continious_key_names[selected_model])

selected_y_axis='tbr'

color_by = st.selectbox(label='colour by ', options=catorgorical_key_names[selected_model])

max_vals = plot_graphs(filtered_data, selected_y_axis, selected_x_axis, color_by)

for val in max_vals:
    st.write(' Maximum TBR for ' ,val[0], ' = ',val[1] )
