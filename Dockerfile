# build with
#     sudo docker build -t openmcworkshop/openmc_nndc_freecad:latest . 
# 

FROM openmcworkshop/openmc_nndc

COPY *.py .
ENTRYPOINT ['python', 'flask_api_for_tbr_simulation.py']

