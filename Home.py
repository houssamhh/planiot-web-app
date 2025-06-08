# -*- coding: utf-8 -*-
"""
Created on Tue Jun  3 11:48:55 2025

@author: houss
"""

import streamlit as st
import pandas as pd
import numpy as np
import subprocess



import scripts.plots as plots


st.set_page_config(
    page_title="Prototypes Demo",
)

st.sidebar.success("Select a project to view.")

st.title('''This Web app showcases the EDICT and PlanIoT prototypes, developped by Houssam Hajj Hassan.
         ''')
         
st.write('''You can view one of the projects by selecting it on the left menu.''')
st.markdown('''You can contact me on: <a href="mailto:houssam.hajj_hassan@telecom-sudparis.eu">houssam.hajj_hassan@telecom-sudparis.eu</a>''', unsafe_allow_html=True)


# all_policies = ["no policy", "PlanIoT", "max-min", "prioritizeTopics", "RL (with additional resources)"]
  
# resp_times_array = np.asarray(plots.get_medium_load_latencies())
# data = pd.DataFrame(np.transpose(resp_times_array), columns=all_policies)

# st.set_page_config(layout="wide",)
# st.title("PlanIoT: AI-driven Adaptation of Edge Infrastructures in IoT Spaces")
# st.write('''PlanIoT is a framework-based solution that enables adaptive IoT data flow management using AI Planning and Reinforcement Learning. 
#          This is achieved via the following core software components: 
#          \n(i) a queueing network composer
#          \n(ii) an AI planner
#          \n(iii) an RL-based resource manager.
#          \nPlanIoT relies on the publish/subscribe paradigm to model IoT data exchange in smart spaces.''')
         
# st.image("./figures/planiot-architecture.png", caption="The PlanIoT high-level architecture.")


# st.write('''
#          We consider 3 scenarios in the evaluation of PlanIoT:
#          1. Normal operations, where we have a medium-loaded data exchange system
#          2. A scalability analysis where the number of subscriptions increases, overwhelming the data exchange system
#          3. A demonstration of PlanIoT's adaptation capabilities with an emergency scenario where a new application category is added.
#          ''')
# tab1, tab2, tab3 = st.tabs(["1. Normal Operations", "2. Scalability Analysis", "3. Adaptation Capabilities"])

# with tab1:
#     st.write('''This scenario considers a medium-loaded data exchange infrastructure. IoT devices publish data to 30 topics, creating a load of 121 MB/s. 
#              16 applications from 4 categories (Analytics, Realtime, Transactional, Videostreaming) subscribe to topics to receive data of interest; the total number of subscriptions is 80.
             
#              ''')
             
#     st.write('''To find the best data exchange configuration that satisfies the QoS requirements of all applications, you can use the AI planner:
#              ''')
             
#     # st.button("Run AI Planner", type="secondary")
    
#     left, right = st.columns(2)
#     if left.button("Run PlanIoT", type="primary"):
#         result = subprocess.Popen(['bash', ' ./Scripts/run_planner.sh Scenarios/medium-load/dataset/response-times-dataset.csv Scenarios/medium-load/pddl-templates/domain-template.pddl Scenarios/medium-load/pddl-templates/problem-template.pddl'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#         stdout, stderr = result.communicate()
        
#         st.write("Testing")
#         # Display the terminal output
#         st.text('\n'.join(stdout.decode().split('\n')[1:][:-1]))
        
#     if right.button("Compare Response Times", type="primary"):
#         tab1.bar_chart(data, height=250, stack=False)

# with tab2:
    
#     st.write('''
#              This scenario considers an increasing number of subscriptions that overwhelm the data exchange system.
#              This use case showcases how PlanIoT Intelligent Resource Manager enables can adaptively scale up resources to satisfy QoS requirements of applications.
#              ''')
#     left2, right2 = st.columns(2)         
#     if left2.button("2. Run PlanIoT", type="primary"):
#         st.write("PlanIoT Output")
#     if right2.button("2. Compare Response Times", type="primary"):    
#         all_subs = ['20', '40', '60', '80', '100']
#         st.pyplot(plots.get_response_time_evolution_fig())
    
# with tab3:
#     col1, col2 = st.columns(2)
#     with col1:
#         st.pyplot(plots.get_emergency_fig())
    


