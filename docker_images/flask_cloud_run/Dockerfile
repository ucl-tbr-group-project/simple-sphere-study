
FROM openmcworkshop/openmc_nndc
RUN pip3 install flask
RUN pip3 install neutronics_material_maker
RUN git clone https://github.com/Shimwell/simple_sphere_TBR_study.git

ENTRYPOINT ["python3", "simple_sphere_TBR_study/flask_api_for_tbr_simulation.py"]
