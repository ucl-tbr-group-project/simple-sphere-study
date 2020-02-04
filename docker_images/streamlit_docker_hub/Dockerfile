
FROM openmcworkshop/openmc_nndc
RUN pip3 install flask
RUN git clone https://github.com/Shimwell/simple_sphere_TBR_study.git
RUN pip3 install neutronics_material_maker
ENTRYPOINT ["streamlit", "run", "simple_sphere_TBR_study/gui_for_simulation.py"]
