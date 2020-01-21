# build with
#     sudo docker build -t openmcworkshop/openmc_nndc_freecad:latest . 
# 

FROM openmcworkshop/openmc_nndc
RUN pip3 install flask
COPY *.py ./
# CMD ['python flask_api_for_tbr_simulation.py']

 ENTRYPOINT ["python3", "flask_api_for_tbr_simulation.py"]
