import streamlit as st
import pandas as pd
import numpy as np
import subprocess



import scripts.plots as plots

# st.set_page_config(
#     page_title="PlanIoT"
# )



def run_planiot():
    subprocess.run(["sudo", "sed", "-i", "s/\r$//", "scripts/run_planner.sh"])
    subprocess.run(["sudo", "chown", "-R", "planiot:planiot", "/home/planiot/planiot/Scenarios"])
    subprocess.run(["sudo", "python", "scripts/InstantiatePddlTemplates.py", "Scenarios/medium-load/dataset/response-times-dataset.csv",
                    "Scenarios/medium-load/pddl-templates/domain-template.pddl",
                    "Scenarios/medium-load/pddl-templates/problem-template.pddl"])
    subprocess.run(["bash", "./scripts/run_planner.sh", "Scenarios/medium-load/pddl-files/domain-generated.pddl",
                    "Scenarios/medium-load/pddl-files/problem-generated.pddl",
                    "Scenarios/medium-load/plans/solution.pddl"])
  
def run_planiot(directory):
    subprocess.run(["sudo", "sed", "-i", "s/\r$//", "scripts/run_planner.sh"])
    subprocess.run(["sudo", "chown", "-R", "planiot:planiot", "/home/planiot/planiot/Scenarios"])
    subprocess.run(["sudo", "python", "scripts/InstantiatePddlTemplates.py", "Scenarios/{}/dataset/response-times-dataset.csv".format(directory),
                    "Scenarios/{}/pddl-templates/domain-template.pddl".format(directory),
                    "Scenarios/{}/pddl-templates/problem-template.pddl".format(directory)])
    subprocess.run(["bash", "./scripts/run_planner.sh", "Scenarios/{}/pddl-files/domain-generated.pddl".format(directory),
                    "Scenarios/{}/pddl-files/problem-generated.pddl".format(directory),
                    "Scenarios/{}/plans/solution.pddl".format(directory)])

def run_planiot_overloaded(directory):
    subprocess.run(["sudo", "sed", "-i", "s/\r$//", "scripts/run_planner.sh"])
    subprocess.run(["sudo", "chown", "-R", "planiot:planiot", "/home/planiot/planiot/Scenarios"])
    subprocess.run(["sudo", "python", "scripts/InstantiatePddlTemplates.py", "Scenarios/{}/dataset/response-times-dataset.csv".format(directory),
                    "Scenarios/{}/pddl-templates/domain-template_overloaded.pddl".format(directory),
                    "Scenarios/{}/pddl-templates/problem-template_overloaded.pddl".format(directory),
                   "-o"])
    subprocess.run(["bash", "./scripts/run_planner.sh", "Scenarios/{}/pddl-files/domain-generated.pddl".format(directory),
                    "Scenarios/{}/pddl-files/problem-generated.pddl".format(directory),
                    "Scenarios/{}/plans/solution.pddl".format(directory)])
all_policies = ["no policy", "PlanIoT", "max-min", "prioritizeTopics", "RL (with additional resources)"]
  
resp_times_array = np.asarray(plots.get_medium_load_latencies())
data = pd.DataFrame(np.transpose(resp_times_array), columns=all_policies)

st.set_page_config(layout="wide", page_title="PlanIoT")
st.title("PlanIoT: AI-driven Adaptation of Edge Infrastructures in IoT Spaces")
st.write('''PlanIoT is a framework-based solution that enables adaptive IoT data flow management using AI Planning and Reinforcement Learning. 
         This is achieved via the following core software components: 
         \n(1) a queueing network composer
         \n(2) an AI planner
         \n(3) an RL-based resource manager.
         \nPlanIoT relies on the publish/subscribe paradigm to model IoT data exchange in smart spaces.''')
         
st.image("./figures/planiot-architecture.png", caption="The PlanIoT high-level architecture.")


st.write('''
         We consider 3 scenarios in the evaluation of PlanIoT:
         1. Normal operations, where we have a medium-loaded data exchange system
         2. A scalability analysis where the number of subscriptions increases, overwhelming the data exchange system
         3. A demonstration of PlanIoT's adaptation capabilities with an emergency scenario where a new application category is added.
         ''')
tab1, tab2, tab3 = st.tabs(["1. Normal Operations", "2. Scalability Analysis", "3. Adaptation Capabilities"])

with tab1:
    st.write('''This scenario considers a medium-loaded data exchange infrastructure. IoT devices publish data to 30 topics, creating a load of 121 MB/s. 
             16 applications from 4 categories (Analytics, Realtime, Transactional, Videostreaming) subscribe to topics to receive data of interest; the total number of subscriptions is 80.
             
             ''')
             
    st.write('''To find the best data exchange configuration that satisfies the QoS requirements of all applications, you can run PlanIoT:
             ''')
             
    # st.button("Run AI Planner", type="secondary")
    
    left, right = st.columns(2)
    if left.button("Run PlanIoT", type="primary"):
        st.write("Running PlanIoT ...")
        run_planiot()
        st.write("You can see PlanIoT's output below:")
        with open("Scenarios/medium-load/plans/solution.pddl") as f:
            st.write(f.read())
        
    if right.button("Compare Response Times", type="primary"):
        tab1.bar_chart(data, height=250, stack=False)

with tab2:
    
    st.write('''
             This scenario considers an increasing number of subscriptions that overwhelm the data exchange system.
             This use case showcases how PlanIoT's Intelligent Resource Manager enables can adaptively scale up resources to satisfy QoS requirements of applications.
             ''')
             
    # st.write('''To find the best data exchange configuration that satisfies the QoS requirements of all applications for this use case, you can run PlanIoT:
    #          ''')
    left2, right2 = st.columns(2)  

    # nb_subs = st.selectbox(
    #           "Select the number of subscriptions:",
    #           ("20", "40", "60", "80", "100"),
    #           index=None,
    #           placeholder="Select the number of subscriptions...",
    #           )       
    # if left2.button("2. Run PlanIoT", type="primary"):
    #     if nb_subs is not None:
    #         directory = "increasing-subscriptions/{}subs".format(nb_subs)
    #         st.write("Running PlanIoT ...")
    #         if (nb_subs in ["20", "40", "60"]):
    #             run_planiot(directory)
    #         else:
    #             run_planiot_overloaded(directory)
    #         st.write("You can see PlanIoT's output below:")
    #         with open("Scenarios/{}/plans/solution.pddl".format(directory)) as f:
    #             st.write(f.read())
    if left2.button("2. Compare Response Times", type="primary"):    
        all_subs = ['20', '40', '60', '80', '100']
        st.pyplot(plots.get_response_time_evolution_fig())
    
with tab3:
    st.write('''
             In the emergency scenario, a new application category (Emergency: EM) is added.
             This use case showcases how PlanIoT can adapt to new applications and requirements.
             ''')
             
    # st.write('''To find the best data exchange configuration that satisfies the QoS requirements of all applications for this use case, you can run PlanIoT:
             # ''')
    # col1, col2 = st.columns(2)
    left3, right3 = st.columns(2)         
    # if left3.button("3. Run PlanIoT", type="primary"):
    #     st.write("PlanIoT Output")
    if left3.button("3. Compare Response Times", type="primary"):     
        with st.columns(2)[1]:
            st.pyplot(plots.get_emergency_fig())
    