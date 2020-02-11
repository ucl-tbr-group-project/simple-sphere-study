
import streamlit as st
import json
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
from tqdm import tqdm
import matplotlib.pyplot as plt

from scipy.stats import norm
from sklearn.neighbors import KernelDensity
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import LeaveOneOut

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
        categorical_key_names = []
        continuous_key_names = []

        for entry in data.keys(): 
                if entry not in ['tbr_error', 'number_of_batches', 'particles_per_batch']:
                        if type(data[entry][0]) == str:
                                categorical_key_names.append(entry)
                        else:
                                continuous_key_names.append(entry)
        return categorical_key_names, continuous_key_names

def plot_histogram():
        # figs = []
        for category in categorical_key_names:
                fig = go.Figure()
                for material in selected_categorical_key_names[category]:

                        print(category, material)


                        y_data = filtered_data[(filtered_data[category] == material)]['tbr']


                        fig.add_trace(go.Histogram(x=y_data,
                                                name= material,
                                                xbins=dict(start=0),
                                                marker_line_width=1.5
                                                )
                                        )
                        try:
                                st.write(' Maximum TBR for ' ,material, ' = ',max(y_data) )
                        except:
                                pass

                fig.update_layout(barmode='overlay',
                                xaxis_title="TBR",
                                yaxis_title="number of simulations",
                                title="Impact of "+category.replace('_',' ')+ " on TBR",
                                showlegend=True,                                
                                )

                fig.update_traces(opacity=0.4)
                # figs.append(fig)
                st.write(fig)

def calculate_bandwidth(data):
        # only uses first 100 values to calculate bandwidth
        bandwidths = 10 ** np.linspace(-1, 1, 100)
        grid = GridSearchCV(KernelDensity(kernel='gaussian'),
                            {'bandwidth': bandwidths},
                            cv=LeaveOneOut())
        grid.fit(data.head(100)[:, None])
        approx_bandwidth = grid.best_params_['bandwidth']
        return approx_bandwidth

def plot_kernel_density():
        # figs = []
        for category in categorical_key_names:
                fig = go.Figure()
                for material in selected_categorical_key_names[category]:

                        data = filtered_data[(filtered_data[category] == material)]['tbr']

                        x_d = np.linspace(min(data), max(data), 500)
                        kde = KernelDensity(bandwidth=calculate_bandwidth(data), kernel='gaussian')
                        kde.fit(data[:, None])
                        logprob = kde.score_samples(x_d[:, None])

                        fig.add_trace(go.Scatter(x=x_d,
                                                 y=np.exp(logprob),
                                                 name=material,
                        ))

                        try:
                                st.write(' Maximum TBR for ' ,material, ' = ',max(x_d) )
                        except:
                                pass

                fig.update_layout(xaxis_title="TBR",
                                  yaxis_title="Number of simulations",
                                  title="Impact of "+category.replace('_', ' ')+ " on TBR",
                                  showlegend=True,
                                  )

                fig.update_traces(opacity=0.5)
                # figs.append(fig)
                st.write(fig)

def perform_data_filtering(filtered_data):
        filters = []
        for key, value in selected_continuous_values.items():
                print('key',key)
                # key_name = entry.key()
                print('value',value)
                # data[]
                filtered_data = filtered_data[(filtered_data[key]>=value[0])&(filtered_data[key]<=value[1])]

        for key, value in selected_categorical_key_names.items():
                print('key',key)
                # key_name = entry.key()
                print('value',value)
                # data[]
                # if len(value) != 0:
                filtered_data = filtered_data[(filtered_data[key].isin(value))]


        st.write(' Number of simulations matching criteria ' ,len(filtered_data), ' from ', len(data), 'simulations')
        st.write(filtered_data)
        return filtered_data


def write_multiselect_boxes():
        selected_categorical_key_names = {}

        for key_name in categorical_key_names:

                defaults = list(data[key_name].unique())

                selected_categorical_key_names[key_name] = st.multiselect(
                                                                        label = key_name.replace('_',' '), 
                                                                        default=list(defaults),
                                                                        options=list(data[key_name].unique())
                                                                        )
        return selected_categorical_key_names


def write_slider_bars():
        selected_continuous_values = {}
        for key_name in continuous_key_names:

                        cleaned_key_name = key_name.replace('_', ' ')

                        min_val = min(data[key_name])
                        max_val = max(data[key_name])

                        if min_val != max_val:
                                selected = st.slider('select a range of ' + str(cleaned_key_name), min_val, max_val, (min_val, max_val))

                                selected_continuous_values[key_name] = selected
        return selected_continuous_values

def draw_model_diagram():
        if selected_categorical_key_names['model'] != None:

                if len(selected_categorical_key_names['model']) == 1:
                        st.image('./images/'+selected_categorical_key_names['model'][0]+'.png')
                if len(selected_categorical_key_names['model']) == 2:
                        st.image('./images/both.png')



data = load_data()

st.title('TBR results explorer')
st.text('Filter a dataset of '+str(len(data))+ ' simulations')

categorical_key_names, continuous_key_names = find_type_of_entries_in_each_field()


selected_categorical_key_names = write_multiselect_boxes()

draw_model_diagram()

selected_continuous_values = write_slider_bars()

filtered_data = perform_data_filtering(data)

# if st.button("Plot histogram"):
#         plot_histogram()

# if st.button("Plot Kernel Density"):
plot_kernel_density()
