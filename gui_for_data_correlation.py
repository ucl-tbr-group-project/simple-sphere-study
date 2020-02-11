
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
        print(results_df)
        return results_df


@st.cache
def find_type_of_entries_in_each_field():
        catorgorical_key_names = []
        continious_key_names = []

        for entry in data.keys(): 
                if entry not in ['tbr_error', 'number_of_batches', 'particles_per_batch']:
                        if type(data[entry][0]) == str:
                                catorgorical_key_names.append(entry)
                        else:
                                continious_key_names.append(entry)
        return catorgorical_key_names, continious_key_names

def plot_graphs():

            max_vals = []
            fig = go.Figure()

            for material in data[color_by].unique():

                    print(color_by, material)

                    y_data = data[(data[color_by] == material)][selected_y_axis]
                    x_data = data[(data[color_by] == material)][selected_x_axis]

                    fig.add_trace(go.Scatter(x=x_data,
                                             y=y_data,
                                            name= material,
                                            mode='markers',
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

            return max_vals


def write_select_boxes():


        selected_x_axis = st.selectbox(
                                                                label = 'x axis', 
                                                                options=continious_key_names
                                                                )
        # selected_y_axis = st.selectbox(
        #                                                         label = 'y axis', 
        #                                                         options=continious_key_names,
        #                                                         )
        return selected_x_axis, 'tbr'



data = load_data()

st.title('TBR correlation explorer')
st.text('Filter a dataset of '+str(len(data))+ ' simulations')

catorgorical_key_names, continious_key_names = find_type_of_entries_in_each_field()

selected_x_axis, selected_y_axis = write_select_boxes()

color_by = st.selectbox(label='colour by ', options=catorgorical_key_names)

max_vals = plot_graphs()

for val in max_vals:
    st.write(' Maximum TBR for ' ,val[0], ' = ',val[1] )
