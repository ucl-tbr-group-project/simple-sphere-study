
FROM openmcworkshop/openmc_nndc
RUN pip3 install flask
RUN pip3 install neutronics_material_maker
RUN pip3 install streamlit

RUN git clone https://github.com/Shimwell/simple_sphere_TBR_study.git

WORKDIR /simple_sphere_TBR_study

ENTRYPOINT ["streamlit", "run", "gui_for_simulation.py"]
