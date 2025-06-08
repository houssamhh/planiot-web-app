# -*- coding: utf-8 -*-
"""
Created on Fri Jun  6 18:07:37 2025

@author: houss
"""

import csv

import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

import numpy as np 


def get_app_categories(app_categories_file):
    appCategories = dict()
    with open (app_categories_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            app = row['app']
            category = row['category']
            appCategories[app] = category
    return appCategories

def get_response_times_per_subscription(fileName, app_categories_file):
    responseTimes = dict()
    categories = get_app_categories(app_categories_file)
    with open (fileName, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            topic = row['topic']
            app = row['app']
            responsetime = row['response_time']
            cat = categories[app]
            responseTimes[topic + '_' + app + '_' + cat] = float(responsetime)
        return responseTimes
    
def get_response_times_per_category(fileName, app_categories_file):
    responseTimes = get_response_times_per_subscription(fileName, app_categories_file)
    categories = get_app_categories(app_categories_file)
    nbAN, nbRT, nbTS, nbVS = 0, 0, 0, 0
    for app in responseTimes.keys():
        cat = categories[app.split('_')[1]]
        if cat == 'AN':
            nbAN += 1
        elif cat == 'RT':
            nbRT += 1
        elif cat == 'TS':
            nbTS += 1
        elif cat == 'VS':
            nbVS += 1
    responsetimeAN, responsetimeRT, responsetimeTS, responsetimeVS = 0, 0, 0, 0
    for subscription, value in responseTimes.items():
        app = subscription.split('_')[1]
        if categories[app] == 'AN':
            responsetimeAN += value
        elif categories[app] == 'RT':
            responsetimeRT += value
        elif categories[app] == 'TS':
            responsetimeTS += value
        elif categories[app] == 'VS':
            responsetimeVS += value
    responsetimeAN = responsetimeAN / nbAN
    responsetimeRT = responsetimeRT / nbRT
    responsetimeTS = responsetimeTS / nbTS
    responsetimeVS = responsetimeVS / nbVS
    return responsetimeAN, responsetimeRT, responsetimeTS, responsetimeVS


def get_response_times_per_category_emergency(fileName, app_categories_file):
    responseTimes = get_response_times_per_subscription(fileName, app_categories_file)
    categories = get_app_categories(app_categories_file)
    nbAN, nbRT, nbTS, nbVS, nbEM = 0, 0, 0, 0, 0
    for app in responseTimes.keys():
        cat = categories[app.split('_')[1]]
        if cat == 'AN':
            nbAN += 1
        elif cat == 'RT':
            nbRT += 1
        elif cat == 'TS':
            nbTS += 1
        elif cat == 'VS':
            nbVS += 1
        elif cat == 'EM':
            nbEM += 1
    responsetimeAN, responsetimeRT, responsetimeTS, responsetimeVS, responsetimeEM = 0, 0, 0, 0, 0
    for subscription, value in responseTimes.items():
        app = subscription.split('_')[1]
        if categories[app] == 'AN':
            responsetimeAN += value
        elif categories[app] == 'RT':
            responsetimeRT += value
        elif categories[app] == 'TS':
            responsetimeTS += value
        elif categories[app] == 'VS':
            responsetimeVS += value
        elif categories[app] == 'EM':
            responsetimeEM += value
    responsetimeAN = responsetimeAN / nbAN
    responsetimeRT = responsetimeRT / nbRT
    responsetimeTS = responsetimeTS / nbTS
    responsetimeVS = responsetimeVS / nbVS
    if nbEM == 0:
        responsetimeEM = 0
    else:
        responsetimeEM = responsetimeEM / nbEM
    return responsetimeAN, responsetimeRT, responsetimeTS, responsetimeVS, responsetimeEM



def get_medium_load_latencies():
    
    app_categories_file = 'Scenarios/medium-load/app_categories.csv'
    planiot_medium_load_directory = 'Scenarios/medium-load/dataset/'
    
    baseline_file_path = planiot_medium_load_directory + 'metrics_baseline.csv'
    planiot_file_path = planiot_medium_load_directory + 'metrics_planner.csv'
    rl_file_path = 'Scenarios/medium-load/dataset/default-440.jsimg-result.jsim'
    maxmin_file_path =  planiot_medium_load_directory + 'metrics_maxmin.csv'
    prioTopics_file_path =  planiot_medium_load_directory + 'metrics_prioritizeTopics.csv'
    
    
    responseTimes_baseline = list(get_response_times_per_category(baseline_file_path, app_categories_file))
    responseTimes_planiot = list(get_response_times_per_category(planiot_file_path, app_categories_file))
    responseTimes_maxmin = list(get_response_times_per_category(maxmin_file_path, app_categories_file))
    responseTimes_prioTopics = list(get_response_times_per_category(prioTopics_file_path,app_categories_file))
    responseTimes_rl = list(get_response_times_per_category(rl_file_path, app_categories_file))
    
    
    return responseTimes_baseline, responseTimes_planiot, responseTimes_maxmin, responseTimes_prioTopics, responseTimes_rl


def get_response_time_evolution_fig():
    
    qos_RT = [0.4, 0.4, 0.4, 0.4, 0.4]
    qos_AN = [1000, 1000, 1000, 1000, 1000]
    qos_VS = [2, 2, 2, 2, 2]
    qos_TS = [4, 4, 4, 4, 4]
    
    app_categories_file = 'Scenarios/increasing-subscriptions/app_categories.csv'

    baseline_20subs_file = 'Scenarios/increasing-subscriptions/20subs/dataset/default-20subs-300.jsimg-result.jsim'
    baseline_40subs_file = 'Scenarios/increasing-subscriptions/40subs/dataset/default-40subs-300.jsimg-result.jsim'
    baseline_60subs_file = 'Scenarios/increasing-subscriptions/60subs/dataset/default-60subs-300.jsimg-result.jsim'
    baseline_80subs_file = 'Scenarios/increasing-subscriptions/80subs/dataset/default-80subs-300.jsimg-result.jsim'
    baseline_100subs_file = 'Scenarios/increasing-subscriptions/100subs/dataset/default-100subs-300.jsimg-result.jsim'
    responseTimes_baseline_20subs = list(get_response_times_per_category(baseline_20subs_file, app_categories_file))
    responseTimes_baseline_40subs = list(get_response_times_per_category(baseline_40subs_file, app_categories_file))
    responseTimes_baseline_60subs = list(get_response_times_per_category(baseline_60subs_file, app_categories_file))
    responseTimes_baseline_80subs = list(get_response_times_per_category(baseline_80subs_file, app_categories_file))
    responseTimes_baseline_100subs = list(get_response_times_per_category(baseline_100subs_file, app_categories_file))
    baseline_20subs_AN = responseTimes_baseline_20subs[0]
    baseline_40subs_AN = responseTimes_baseline_40subs[0]
    baseline_60subs_AN = responseTimes_baseline_60subs[0]
    baseline_80subs_AN = responseTimes_baseline_80subs[0]
    baseline_100subs_AN = responseTimes_baseline_100subs[0]
    baseline_20subs_RT = responseTimes_baseline_20subs[1]
    baseline_40subs_RT = responseTimes_baseline_40subs[1]
    baseline_60subs_RT = responseTimes_baseline_60subs[1]
    baseline_80subs_RT = responseTimes_baseline_80subs[1]
    baseline_100subs_RT = responseTimes_baseline_100subs[1]
    baseline_20subs_TS = responseTimes_baseline_20subs[2]
    baseline_40subs_TS = responseTimes_baseline_40subs[2]
    baseline_60subs_TS = responseTimes_baseline_60subs[2]
    baseline_80subs_TS = responseTimes_baseline_80subs[2]
    baseline_100subs_TS = responseTimes_baseline_100subs[2]
    baseline_20subs_VS = responseTimes_baseline_20subs[3]
    baseline_40subs_VS = responseTimes_baseline_40subs[3]
    baseline_60subs_VS = responseTimes_baseline_60subs[3]
    baseline_80subs_VS = responseTimes_baseline_80subs[3]
    baseline_100subs_VS = responseTimes_baseline_100subs[3]
    
    planner_20subs_file = 'Scenarios/increasing-subscriptions/20subs/dataset/plannerConfiguration-20subs-300.jsimg-result.jsim'
    planner_40subs_file = 'Scenarios/increasing-subscriptions/40subs/dataset/plannerConfiguration-40subs-300.jsimg-result.jsim'
    planner_60subs_file = 'Scenarios/increasing-subscriptions/60subs/dataset/plannerConfiguration-60subs-300.jsimg-result.jsim'
    planner_80subs_file = 'Scenarios/increasing-subscriptions/80subs/dataset/plannerConfiguration-80subs-300.jsimg-result.jsim'
    planner_100subs_file = 'Scenarios/increasing-subscriptions/100subs/dataset/plannerConfiguration-100subs-300.jsimg-result.jsim'

    responseTimes_planner_20subs = list(get_response_times_per_category(planner_20subs_file, app_categories_file))
    responseTimes_planner_40subs = list(get_response_times_per_category(planner_40subs_file, app_categories_file))
    responseTimes_planner_60subs = list(get_response_times_per_category(planner_60subs_file, app_categories_file))
    responseTimes_planner_80subs = list(get_response_times_per_category(planner_80subs_file, app_categories_file))
    responseTimes_planner_100subs = list(get_response_times_per_category(planner_100subs_file, app_categories_file))
    planner_20subs_AN = responseTimes_planner_20subs[0]
    planner_40subs_AN = responseTimes_planner_40subs[0]
    planner_60subs_AN = responseTimes_planner_60subs[0]
    planner_80subs_AN = responseTimes_planner_80subs[0]
    planner_100subs_AN = responseTimes_planner_100subs[0]
    planner_20subs_RT = responseTimes_planner_20subs[1]
    planner_40subs_RT = responseTimes_planner_40subs[1]
    planner_60subs_RT = responseTimes_planner_60subs[1]
    planner_80subs_RT = responseTimes_planner_80subs[1]
    planner_100subs_RT = responseTimes_planner_100subs[1]
    planner_20subs_TS = responseTimes_planner_20subs[2]
    planner_40subs_TS = responseTimes_planner_40subs[2]
    planner_60subs_TS = responseTimes_planner_60subs[2]
    planner_80subs_TS = responseTimes_planner_80subs[2]
    planner_100subs_TS = responseTimes_planner_100subs[2]
    planner_20subs_VS = responseTimes_planner_20subs[3]
    planner_40subs_VS = responseTimes_planner_40subs[3]
    planner_60subs_VS = responseTimes_planner_60subs[3]
    planner_80subs_VS = responseTimes_planner_80subs[3]
    planner_100subs_VS = responseTimes_planner_100subs[3]
    
    
    #1 New Approach with RL
    new_20subs_file = 'Scenarios/increasing-subscriptions/20subs/dataset/plannerConfiguration-20subs-300.jsimg-result.jsim'
    new_40subs_file = 'Scenarios/increasing-subscriptions/40subs/dataset/plannerConfiguration-40subs-300.jsimg-result.jsim'
    new_60subs_file = 'Scenarios/increasing-subscriptions/60subs/dataset/plannerConfiguration-60subs-300.jsimg-result.jsim'
    new_80subs_file = 'Scenarios/increasing-subscriptions/80subs/dataset/plannerConfiguration-80subs-500.jsimg-result.jsim'
    new_100subs_file = 'Scenarios/increasing-subscriptions/100subs/dataset/plannerConfiguration-100subs-500.jsimg-result.jsim'
    responseTimes_new_20subs = list(get_response_times_per_category(new_20subs_file, app_categories_file))
    responseTimes_new_40subs = list(get_response_times_per_category(new_40subs_file, app_categories_file))
    responseTimes_new_60subs = list(get_response_times_per_category(new_60subs_file, app_categories_file))
    responseTimes_new_80subs = list(get_response_times_per_category(new_80subs_file, app_categories_file))
    responseTimes_new_100subs = list(get_response_times_per_category(new_100subs_file, app_categories_file))
    new_20subs_AN = responseTimes_new_20subs[0]
    new_40subs_AN = responseTimes_new_40subs[0]
    new_60subs_AN = responseTimes_new_60subs[0]
    new_80subs_AN = responseTimes_new_80subs[0]
    new_100subs_AN = responseTimes_new_100subs[0]
    new_20subs_RT = responseTimes_new_20subs[1]
    new_40subs_RT = responseTimes_new_40subs[1]
    new_60subs_RT = responseTimes_new_60subs[1]
    new_80subs_RT = responseTimes_new_80subs[1]
    new_100subs_RT = responseTimes_new_100subs[1]
    new_20subs_TS = responseTimes_new_20subs[2]
    new_40subs_TS = responseTimes_new_40subs[2]
    new_60subs_TS = responseTimes_new_60subs[2]
    new_80subs_TS = responseTimes_new_80subs[2]
    new_100subs_TS = responseTimes_new_100subs[2]
    new_20subs_VS = responseTimes_new_20subs[3]
    new_40subs_VS = responseTimes_new_40subs[3]
    new_60subs_VS = responseTimes_new_60subs[3]
    new_80subs_VS = responseTimes_new_80subs[3]
    new_100subs_VS = responseTimes_new_100subs[3]
    
    maxmin_20subs_file = 'Scenarios/increasing-subscriptions/20subs/dataset/maxmin-20subs-300.jsimg-result.jsim'
    maxmin_40subs_file = 'Scenarios/increasing-subscriptions/40subs/dataset/maxmin-40subs-300.jsimg-result.jsim'
    maxmin_60subs_file = 'Scenarios/increasing-subscriptions/60subs/dataset/maxmin-60subs-300.jsimg-result.jsim'
    maxmin_80subs_file = 'Scenarios/increasing-subscriptions/80subs/dataset/maxmin-80subs-300.jsimg-result.jsim'
    maxmin_100subs_file = 'Scenarios/increasing-subscriptions/100subs/dataset/maxmin-100subs-300.jsimg-result.jsim'


    responseTimes_maxmin_20subs = list(get_response_times_per_category(maxmin_20subs_file, app_categories_file))
    responseTimes_maxmin_40subs = list(get_response_times_per_category(maxmin_40subs_file, app_categories_file))
    responseTimes_maxmin_60subs = list(get_response_times_per_category(maxmin_60subs_file, app_categories_file))
    responseTimes_maxmin_80subs = list(get_response_times_per_category(maxmin_80subs_file, app_categories_file))
    responseTimes_maxmin_100subs = list(get_response_times_per_category(maxmin_100subs_file, app_categories_file))

    maxmin_20subs_AN = responseTimes_maxmin_20subs[0]
    maxmin_40subs_AN = responseTimes_maxmin_40subs[0]
    maxmin_60subs_AN = responseTimes_maxmin_60subs[0]
    maxmin_80subs_AN = responseTimes_maxmin_80subs[0]
    maxmin_100subs_AN = responseTimes_maxmin_100subs[0]
    maxmin_20subs_RT = responseTimes_maxmin_20subs[1]
    maxmin_40subs_RT = responseTimes_maxmin_40subs[1]
    maxmin_60subs_RT = responseTimes_maxmin_60subs[1]
    maxmin_80subs_RT = responseTimes_maxmin_80subs[1]
    maxmin_100subs_RT = responseTimes_maxmin_100subs[1]
    maxmin_20subs_TS = responseTimes_maxmin_20subs[2]
    maxmin_40subs_TS = responseTimes_maxmin_40subs[2]
    maxmin_60subs_TS = responseTimes_maxmin_60subs[2]
    maxmin_80subs_TS = responseTimes_maxmin_80subs[2]
    maxmin_100subs_TS = responseTimes_maxmin_100subs[2]
    maxmin_20subs_VS = responseTimes_maxmin_20subs[3]
    maxmin_40subs_VS = responseTimes_maxmin_40subs[3]
    maxmin_60subs_VS = responseTimes_maxmin_60subs[3]
    maxmin_80subs_VS = responseTimes_maxmin_80subs[3]
    maxmin_100subs_VS = responseTimes_maxmin_100subs[3]
    
    prioTopics_20subs_file = 'Scenarios/increasing-subscriptions/20subs/dataset/prioritizeTopics-20subs-300.jsimg-result.jsim'
    prioTopics_40subs_file = 'Scenarios/increasing-subscriptions/40subs/dataset/prioritizeTopics-40subs-300.jsimg-result.jsim'
    prioTopics_60subs_file = 'Scenarios/increasing-subscriptions/60subs/dataset/prioritizeTopics-60subs-300.jsimg-result.jsim'
    prioTopics_80subs_file = 'Scenarios/increasing-subscriptions/80subs/dataset/prioritizeTopics-80subs-300.jsimg-result.jsim'
    prioTopics_100subs_file = 'Scenarios/increasing-subscriptions/100subs/dataset/prioritizeTopics-100subs-300.jsimg-result.jsim'

    responseTimes_prioTopics_20subs = list(get_response_times_per_category(prioTopics_20subs_file, app_categories_file))
    responseTimes_prioTopics_40subs = list(get_response_times_per_category(prioTopics_40subs_file, app_categories_file))
    responseTimes_prioTopics_60subs = list(get_response_times_per_category(prioTopics_60subs_file, app_categories_file))
    responseTimes_prioTopics_80subs = list(get_response_times_per_category(prioTopics_80subs_file, app_categories_file))
    responseTimes_prioTopics_100subs = list(get_response_times_per_category(prioTopics_100subs_file, app_categories_file))
    prioTopics_20subs_AN = responseTimes_prioTopics_20subs[0]
    prioTopics_40subs_AN = responseTimes_prioTopics_40subs[0]
    prioTopics_60subs_AN = responseTimes_prioTopics_60subs[0]
    prioTopics_80subs_AN = responseTimes_prioTopics_80subs[0]
    prioTopics_100subs_AN = responseTimes_prioTopics_100subs[0]
    prioTopics_20subs_RT = responseTimes_prioTopics_20subs[1]
    prioTopics_40subs_RT = responseTimes_prioTopics_40subs[1]
    prioTopics_60subs_RT = responseTimes_prioTopics_60subs[1]
    prioTopics_80subs_RT = responseTimes_prioTopics_80subs[1]
    prioTopics_100subs_RT = responseTimes_prioTopics_100subs[1]
    prioTopics_20subs_TS = responseTimes_prioTopics_20subs[2]
    prioTopics_40subs_TS = responseTimes_prioTopics_40subs[2]
    prioTopics_60subs_TS = responseTimes_prioTopics_60subs[2]
    prioTopics_80subs_TS = responseTimes_prioTopics_80subs[2]
    prioTopics_100subs_TS = responseTimes_prioTopics_100subs[2]
    prioTopics_20subs_VS = responseTimes_prioTopics_20subs[3]
    prioTopics_40subs_VS = responseTimes_prioTopics_40subs[3]
    prioTopics_60subs_VS = responseTimes_prioTopics_60subs[3]
    prioTopics_80subs_VS = responseTimes_prioTopics_80subs[3]
    prioTopics_100subs_VS = responseTimes_prioTopics_100subs[3]
    
    
    
    baseline_RT = [baseline_20subs_RT, baseline_40subs_RT, baseline_60subs_RT, baseline_80subs_RT, baseline_100subs_RT]
    planner_RT = [planner_20subs_RT, planner_40subs_RT, planner_60subs_RT, planner_80subs_RT, planner_100subs_RT]
    new_RT = [new_20subs_RT, new_40subs_RT, new_60subs_RT, new_80subs_RT, new_100subs_RT]
    maxmin_RT = [maxmin_20subs_RT, maxmin_40subs_RT, maxmin_60subs_RT, maxmin_80subs_RT, maxmin_100subs_RT]
    prioTopics_RT = [prioTopics_20subs_RT, prioTopics_40subs_RT, prioTopics_60subs_RT, prioTopics_80subs_RT, prioTopics_100subs_RT]
    
    responsetimes_RT = np.array([baseline_RT, planner_RT, new_RT, maxmin_RT, prioTopics_RT])
    
    baseline_AN = [baseline_20subs_AN, baseline_40subs_AN, baseline_60subs_AN, baseline_80subs_AN, baseline_100subs_AN]
    planner_AN = [planner_20subs_AN, planner_40subs_AN, planner_60subs_AN, planner_80subs_AN, planner_100subs_AN]
    new_AN = [new_20subs_AN, new_40subs_AN, new_60subs_AN, new_80subs_AN, new_100subs_AN]
    maxmin_AN = [maxmin_20subs_AN, maxmin_40subs_AN, maxmin_60subs_AN, maxmin_80subs_AN, maxmin_100subs_AN]
    prioTopics_AN = [prioTopics_20subs_AN, prioTopics_40subs_AN, prioTopics_60subs_AN, prioTopics_80subs_AN, prioTopics_100subs_AN]
    
    responsetimes_AN = np.array([baseline_AN, planner_AN, new_AN, maxmin_AN, prioTopics_AN])
    
    baseline_TS = [baseline_20subs_TS, baseline_40subs_TS, baseline_60subs_TS, baseline_80subs_TS, baseline_100subs_TS]
    planner_TS = [planner_20subs_TS, planner_40subs_TS, planner_60subs_TS, planner_80subs_TS, planner_100subs_TS]
    new_TS = [new_20subs_TS, new_40subs_TS, new_60subs_TS, new_80subs_TS, new_100subs_TS]  
    maxmin_TS = [maxmin_20subs_TS, maxmin_40subs_TS, maxmin_60subs_TS, maxmin_80subs_TS, maxmin_100subs_TS]
    prioTopics_TS = [prioTopics_20subs_TS, prioTopics_40subs_TS, prioTopics_60subs_TS, prioTopics_80subs_TS, prioTopics_100subs_TS]
    
    responsetimes_TS = np.array([baseline_TS, planner_TS, new_TS, maxmin_TS, prioTopics_TS])
        
    baseline_VS = [baseline_20subs_VS, baseline_40subs_VS, baseline_60subs_VS, baseline_80subs_VS, baseline_100subs_VS]
    planner_VS = [planner_20subs_VS, planner_40subs_VS, planner_60subs_VS, planner_80subs_VS, planner_100subs_VS]
    new_VS = [new_20subs_VS, new_40subs_VS, new_60subs_VS, new_80subs_VS, new_100subs_VS]
    maxmin_VS = [maxmin_20subs_VS, maxmin_40subs_VS, maxmin_60subs_VS, maxmin_80subs_VS, maxmin_100subs_VS]
    prioTopics_VS = [prioTopics_20subs_VS, prioTopics_40subs_VS, prioTopics_60subs_VS, prioTopics_80subs_VS, prioTopics_100subs_VS]
    
    responsetimes_VS = np.array([baseline_VS, planner_VS, new_VS, maxmin_VS, prioTopics_VS])
        
    x_axis = [20, 40, 60, 80, 100]
    x = np.array([20, 40, 60, 80, 100])
    fig, ax = plt.subplots(4, 1, sharex=True)
    X_ = np.linspace(x.min(), x.max(), 15)
    
    baseline_AN_spline = make_interp_spline(x_axis, baseline_AN)
    baseline_AN_smoothed = baseline_AN_spline(X_)
    baseline_RT_spline = make_interp_spline(x_axis, baseline_RT)
    baseline_RT_smoothed = baseline_RT_spline(X_)
    baseline_TS_spline = make_interp_spline(x_axis, baseline_TS)
    baseline_TS_smoothed = baseline_TS_spline(X_)
    baseline_VS_spline = make_interp_spline(x_axis, baseline_VS)
    baseline_VS_smoothed = baseline_VS_spline(X_)
    
    
    planner_AN_spline = make_interp_spline(x_axis, planner_AN)
    planner_AN_smoothed = planner_AN_spline(X_)
    planner_RT_spline = make_interp_spline(x_axis, planner_RT)
    planner_RT_smoothed = planner_RT_spline(X_)
    planner_TS_spline = make_interp_spline(x_axis, planner_TS)
    planner_TS_smoothed = planner_TS_spline(X_)
    planner_VS_spline = make_interp_spline(x_axis, planner_VS)
    planner_VS_smoothed = planner_VS_spline(X_)

    new_AN_spline = make_interp_spline(x_axis, new_AN)
    new_AN_smoothed = new_AN_spline(X_)
    new_RT_spline = make_interp_spline(x_axis, new_RT)
    new_RT_smoothed = new_RT_spline(X_)
    new_TS_spline = make_interp_spline(x_axis, new_TS)
    new_TS_smoothed = new_TS_spline(X_)
    new_VS_spline = make_interp_spline(x_axis, new_VS)
    new_VS_smoothed = new_VS_spline(X_)

    prioTopics_AN_spline = make_interp_spline(x_axis, prioTopics_AN)
    prioTopics_AN_smoothed = prioTopics_AN_spline(X_)
    prioTopics_RT_spline = make_interp_spline(x_axis, prioTopics_RT)
    prioTopics_RT_smoothed = prioTopics_RT_spline(X_)
    prioTopics_TS_spline = make_interp_spline(x_axis, prioTopics_TS)
    prioTopics_TS_smoothed = prioTopics_TS_spline(X_)
    prioTopics_VS_spline = make_interp_spline(x_axis, prioTopics_VS)
    prioTopics_VS_smoothed = prioTopics_VS_spline(X_)
    
    
    qos_RT = [0.4, 0.4, 0.4, 0.4, 0.4]
    qos_VS = [2, 2, 2, 2, 2]
    qos_TS = [4, 4, 4, 4, 4]
    qos_RT_spline = make_interp_spline(x_axis, qos_RT)
    qos_RT_smoothed = qos_RT_spline(X_)
    qos_TS_spline = make_interp_spline(x_axis, qos_TS)
    qos_TS_smoothed = qos_TS_spline(X_)
    qos_VS_spline = make_interp_spline(x_axis, qos_VS)
    qos_VS_smoothed = qos_VS_spline(X_)
    
    
    plt.subplot(2, 2, 1)
    plt.plot(X_, baseline_AN_smoothed, color='blue', linewidth=3)
    plt.scatter(x, baseline_AN, label='no policy', color='blue', marker='o', s=90)
    plt.plot(X_, planner_AN_smoothed, color='green', linewidth=3)
    plt.scatter(x, planner_AN, label='PlanIoT', color='green', marker='v', s=90)
    plt.plot(X_, new_AN_smoothed, color='red', linewidth=3)
    plt.scatter(x, new_AN, label='PlanIoT with IRM', color='red', marker='P', s=90)
    plt.plot(X_, prioTopics_AN_smoothed, color='brown', linewidth=3)
    plt.scatter(x, prioTopics_AN, label='topic priorities', color='brown', marker='s', s=90)
    plt.title('AN',  y=0.87, fontsize=24)
    plt.axvspan(80, 100, alpha=0.2, color='red', label='overloaded')
    plt.xticks(fontsize=28)
    plt.xticks([20, 40, 60, 80, 100])
    plt.yticks(fontsize=28)
    
    plt.subplot(2, 2, 2)
    plt.plot(X_, baseline_RT_smoothed, color='blue', linewidth=3)
    plt.scatter(x, baseline_RT, label='baseline', color='blue', marker='o', s=90)
    plt.plot(X_, planner_RT_smoothed, color='green', linewidth=3)
    plt.scatter(x, planner_RT, label='PlanIoT', color='green', marker='v', s=90)
    plt.plot(X_, new_RT_smoothed, color='red', linewidth=3)
    plt.scatter(x, new_RT, label='new approach', color='red', marker='P', s=90)
    plt.plot(X_, prioTopics_RT_smoothed, color='brown', linewidth=3)
    plt.scatter(x, prioTopics_RT, label='topic priorities', color='brown', marker='s', s=90)
    plt.plot(X_, qos_RT_smoothed, '--', label='max. resp. time', linewidth=3.0, color='purple')
    plt.title('RT',  y=0.87, fontsize=24)
    plt.axvspan(80, 100, alpha=0.2, color='red', label='overloaded')
    plt.xticks(fontsize=28)
    plt.xticks([20, 40, 60, 80, 100])
    plt.yticks(fontsize=28)
     
    plt.subplot(2, 2, 3)
    plt.plot(X_, baseline_TS_smoothed, color='blue', linewidth=3)
    plt.scatter(x, baseline_TS, label='baseline', color='blue', marker='o', s=90)
    plt.plot(X_, planner_TS_smoothed, color='green', linewidth=3)
    plt.scatter(x, planner_TS, label='PlanIoT', color='green', marker='v', s=90)
    plt.plot(X_, new_TS_smoothed, color='red', linewidth=3)
    plt.scatter(x, new_TS, label='new approach', color='red', marker='P', s=90)
    plt.plot(X_, prioTopics_TS_smoothed, color='brown', linewidth=3)
    plt.scatter(x, prioTopics_TS, label='topic priorities', color='brown', marker='s', s=90)
    plt.plot(X_, qos_TS_smoothed, '--', label='max. resp. time', linewidth=3.0, color='purple')
    plt.title('TS',  y=0.87, fontsize=24)
    plt.axvspan(80, 100, alpha=0.2, color='red', label='overloaded')
    plt.xticks(fontsize=28)
    plt.xticks([20, 40, 60, 80, 100])

    plt.xlabel('Number of subscriptions', fontsize=28)
    plt.yticks(fontsize=28)
    plt.ylabel('Response time (sec)', fontsize=28, y=0.9)
     
    plt.subplot(2, 2, 4)
    plt.plot(X_, baseline_VS_smoothed, color='blue', linewidth=3)
    plt.scatter(x, baseline_VS, label='no policy', color='blue', marker='o', s=90)
    plt.plot(X_, planner_VS_smoothed, color='green', linewidth=3)
    plt.scatter(x, planner_VS, label='PlanIoT w/o IRM', color='green', marker='v', s=90)
    plt.plot(X_, new_VS_smoothed, color='red', marker='+', linewidth=3)
    plt.scatter(x, new_VS, label='PlanIoT w/ IRM', color='red', marker='P', s=90)
    plt.plot(X_, prioTopics_VS_smoothed, color='brown', linewidth=3)
    plt.scatter(x, prioTopics_VS, label='topic priorities', color='brown', marker='s', s=90)
    plt.plot(X_, qos_VS_smoothed, '--', label='max. resp. time', linewidth=3.0, color='purple')
    plt.title('ST',  y=0.9, fontsize=24)
    plt.axvspan(80, 100, alpha=0.2, color='red', label='overloaded')

    plt.xlabel('Number of subscriptions', fontsize=28)
    plt.legend(loc ='upper left', prop={'size': 16})

    
    plt.xlabel('Number of subscriptions', fontsize=28)
    plt.xticks(fontsize=28)
    plt.xticks([20, 40, 60, 80, 100])
    plt.yticks(fontsize=28)
    fig.set_size_inches(20, 10)
    

    plt.rcParams.update({'font.size': 14})
    fig.tight_layout(pad=1.0,)
    
    return fig
    

def get_emergency_fig():
    
    app_categories_file = 'Senarios/emergency/app_categories.csv'
    emergency_file_path = 'Scenarios/emergency/dataset/metrics_plannerConfiguration.csv'
    validation_file_path = 'Scenarios/increasing-subscriptions/20subs/dataset/metrics_planner.csv'
    responseTimes_emergency = list(get_response_times_per_category_emergency(emergency_file_path, app_categories_file))

    categories = ['AN', 'RT', 'TS', 'VS', 'EM']
    
    fig, ax = plt.subplots(1, 1, sharey=True)
    plt.subplot(1, 1, 1)
    X_axis = np.arange(len(categories))
    # plt.bar(X_axis, responseTimes_validation, 0.2, color='coral', alpha=0.99, hatch = '*', label = 'PlanIoT - emergency')
    plt.bar(X_axis + 0.1, responseTimes_emergency, 0.2, color='coral', alpha=0.99, hatch = '**', label = 'PlanIoT - emergency')
    plt.xticks(X_axis, categories)
    plt.xlabel('Application category')
    plt.ylabel('Response time (in s)')
    plt.xticks(rotation=90)
    plt.legend(loc='upper left')
    plt.rcParams.update({'font.size': 14})
    plt.ylim([0, 7])
    
    
    return fig