import streamlit as st
import subprocess

import pandas as pd

st.set_page_config(layout="wide", page_title="EDICT")
st.title("EDICT: A Simulation Tool for Generating Performance Metrics Datasets in IoT Environments")
st.write('''EDICT is a simulation tool for evaluating the performance of Edge interactions in IoT-enhanced environments.
         EDICT relies on the publish/subscribe paradigm to model data flow interactions in smart spaces, and one queueing network models to model and simualte the performance of IoT data exchange. ''')
         
st.image("./figures/edict-overview-cropped.png", caption="Overview of EDICT's Architecture.")

st.write('''
         Try EDICT by uploading a JSON representation of your IoT system. 
         For more information about how to represent the IoT system, you can visit https://github.com/houssamhh/edict.
         ''')
uploaded_file = st.file_uploader("Upload IoT System Representation")



if st.button("Run Simulation", type="primary"):
    if uploaded_file is not None:
        # chown -R planiot:planiot /home/planiot/planiot/edict
        subprocess.run(["sudo", "chown", "-R", "planiot:planiot", "/home/planiot/planiot/edict"])
        b = uploaded_file.getvalue()
        with open('edict/{}'.format(uploaded_file.name), 'wb') as f: 
            f.write(b)
        st.write("Running EDICT simulation...")    
        subprocess.run(["sudo", "java", "-jar", "edict/edict.jar", "edict/{}".format(uploaded_file.name), "metrics.csv", "20", "user_simulation"]) 
        st.write("Simulation Done!")
        st.write("You can check the results below:")
        df = pd.read_csv("edict/{}".format(uploaded_file.name.replace(".json", "_user_simulation.csv")))
        st.dataframe(df)
    else:
        st.write("Please upload a file to run the simulation.")

