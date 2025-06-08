# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 22:42:33 2024

@author: houss
"""
import csv
import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict
import re
from scipy.interpolate import make_interp_spline

def tryint(s):
    """
    Return an int if possible, or `s` unchanged.
    """
    try:
        return int(s)
    except ValueError:
        return s

def alphanum_key(s):
    """
    Turn a string into a list of string and number chunks.

    >>> alphanum_key("z23a")
    ["z", 23, "a"]

    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

def human_sort(l):
    """
    Sort a list in the way that humans expect.
    """
    l.sort(key=alphanum_key)
    
# app_categories_file = './experiments/medium-load/app_categories.csv'
app_categories_file = './experiments/increasing-subscriptions/app-categories.csv'
resptime_an = dict()
resptime_rt = dict()
resptime_ts = dict()
resptime_vs = dict()
resptime_em = dict()
    
def get_app_categories():
    appCategories = dict()
    with open (app_categories_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            app = row['app']
            category = row['category']
            appCategories[app] = category
    return appCategories

def initialize_dictionaries():
    for i in range (1, 31):
        resptime_an['topic'+str(i)] = list()
        resptime_rt['topic'+str(i)] = list()
        resptime_ts['topic'+str(i)] = list()
        resptime_vs['topic'+str(i)] = list()
        
def get_response_times_per_topic(fileName):
    categories = get_app_categories()
    initialize_dictionaries()
    topic_categories = dict()
    for i in range (1, 31):
        topic_categories['topic'+str(i)] = set()
    # topic_categories['bms'], topic_categories['videosurveillance'], topic_categories['amazonecho'], topic_categories['intrusiondetection'], topic_categories['firedetection'], topic_categories['occupancymanagement'], topic_categories['printing'], topic_categories['smartthings'], topic_categories['energymanagement'] = set(),set(), set(),set(),set(),set(),set(),set(),set()
    with open (fileName, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            topic = row['topic']
            app = row['app']
            responsetime = row['response_time']
            cat = categories[app]
            if (float(responsetime) != 0):
                if cat == 'AN':
                    ls = resptime_an[topic]
                    ls.append(float(responsetime))
                    resptime_an[topic] = ls
                    topics_cats = topic_categories[topic]
                    topics_cats.add('AN')
                    topic_categories[topic] = topics_cats
                elif cat == 'RT':
                    ls = resptime_rt[topic]
                    ls.append(float(responsetime))
                    resptime_rt[topic] = ls
                    topics_cats = topic_categories[topic]
                    topics_cats.add('RT')
                    topic_categories[topic] = topics_cats
                elif cat == 'TS':
                     ls = resptime_ts[topic]
                     ls.append(float(responsetime))
                     resptime_ts[topic] = ls
                     topics_cats = topic_categories[topic]
                     topics_cats.add('TS')
                     topic_categories[topic] = topics_cats
                elif cat == 'VS':
                    ls = resptime_vs[topic]
                    ls.append(float(responsetime))
                    resptime_vs[topic] = ls
                    topics_cats = topic_categories[topic]
                    topics_cats.add('VS')
                    topic_categories[topic] = topics_cats
                elif cat == 'EM':
                    ls = resptime_em[topic]
                    ls.append(float(responsetime))
                    resptime_em[topic] = ls
                    topics_cats = topic_categories[topic]
                    topics_cats.add('EM')
                    topic_categories[topic] = topics_cats
                        

def get_throughputs_per_subscription(fileName):
    throughputs = dict()
    categories = get_app_categories()
    with open (fileName, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            topic = row['topic']
            app = row['app']
            throughput = row['throughput']
            cat = categories[app]
            throughputs[topic + '_' + app] = float(throughput)
    return throughputs

def get_throughput_per_category(fileName):
    throughputs = get_throughputs_per_subscription(fileName)
    categories = get_app_categories()
    nbAN, nbRT, nbTS, nbVS = 0, 0, 0, 0
    for app in throughputs.keys():
        cat = categories[app.split('_')[1]]
        if cat == 'AN':
            nbAN += 1
        elif cat == 'RT':
            nbRT += 1
        elif cat == 'TS':
            nbTS += 1
        elif cat == 'VS':
            nbVS += 1
    thrAN, thrRT, thrTS, thrVS = 0, 0, 0, 0
    for subscription, value in throughputs.items():
        app = subscription.split('_')[1]
        if categories[app] == 'AN':
            thrAN += value
        elif categories[app] == 'RT':
            thrRT += value
        elif categories[app] == 'TS':
            thrTS += value
        elif categories[app] == 'VS':
            thrVS += value
    
    thrAN = thrAN / nbAN
    thrRT = thrRT / nbRT
    thrTS = thrTS / nbTS
    thrVS = thrVS / nbVS
    thrAN = thrAN * 50
    thrRT = thrRT * 50
    thrTS = thrTS * 50
    thrVS = thrVS * 50
    return thrAN, thrRT, thrTS, thrVS

def get_response_times_per_subscription(fileName):
    responseTimes = dict()
    categories = get_app_categories()
    with open (fileName, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            topic = row['topic']
            app = row['app']
            responsetime = row['response_time']
            cat = categories[app]
            responseTimes[topic + '_' + app + '_' + cat] = float(responsetime)
        return responseTimes
    
def get_response_times_per_category(fileName):
    responseTimes = get_response_times_per_subscription(fileName)
    categories = get_app_categories()
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
        elif categories[app] == 'EM':
            responsetimeEM += value
    responsetimeAN = responsetimeAN / nbAN
    responsetimeRT = responsetimeRT / nbRT
    responsetimeTS = responsetimeTS / nbTS
    responsetimeVS = responsetimeVS / nbVS
    # print(nbAN, nbRT, nbTS, nbVS)
    # if nbEM == 0:
    #     responsetimeEM = 0
    # else:
    #     responsetimeEM = responsetimeEM / nbEM
    return responsetimeAN, responsetimeRT, responsetimeTS, responsetimeVS


def bar_chart_medium_load():
    
    planiot_medium_load_directory = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\medium-load\\dataset\\'
    
    baseline_file_path = planiot_medium_load_directory + 'metrics_baseline.csv'
    planiot_file_path = planiot_medium_load_directory + 'metrics_planner.csv'
    rl_file_path = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\medium-load\\jsimg\\default-440.jsimg-result.jsim'
    maxmin_file_path =  planiot_medium_load_directory + 'metrics_maxmin.csv'
    prioTopics_file_path =  planiot_medium_load_directory + 'metrics_prioritizeTopics.csv'
    
    '''BASELINE VS SOTA'''
    
    responseTimes_baseline = list(get_response_times_per_category(baseline_file_path))
    responseTimes_planiot = list(get_response_times_per_category(planiot_file_path))
    responseTimes_maxmin = list(get_response_times_per_category(maxmin_file_path))
    responseTimes_prioTopics = list(get_response_times_per_category(prioTopics_file_path))
    responseTimes_rl = list(get_response_times_per_category(rl_file_path))
    
    
    categories = ['AN', 'RT', 'TS', 'ST']
    #categories = get_response_times_per_subscription(currentNetwork_file_path).keys()
    fig = plt.figure()
    
    X_axis = np.arange(len(categories))
    
    plt.bar(X_axis - 0.2, responseTimes_baseline, 0.2, label = 'no policy', alpha=0.99, hatch = '/', color='blue')
    # plt.bar(X_axis - 0.1, responseTimes_planiot, 0.2, label = 'PlanIoT', alpha=0.99, hatch = '*', color='green')
    plt.bar(X_axis + 0.0, responseTimes_maxmin, 0.2, label = 'max-min', alpha=0.99, hatch = '.', color='orange')
    plt.bar(X_axis + 0.2, responseTimes_prioTopics, 0.2, label = 'prioritize Topics', alpha=0.99, hatch = '+', color='red')
    
    # plt.bar(X_axis - 0.2, responseTimes_baseline, 0.2, label = 'no policy', alpha=0.99, hatch = '/', color='blue')
    # plt.bar(X_axis - 0.0, responseTimes_planiot, 0.2, label = 'PlanIoT', alpha=0.99, hatch = '*', color='green')
    # # plt.bar(X_axis + 0.0, responseTimes_maxmin, 0.2, label = 'max-min', alpha=0.99, hatch = '.', color='orange')
    # plt.bar(X_axis + 0.2, responseTimes_rl, 0.2, label = 'RL approaches', alpha=0.99, hatch = 'o', color='brown')
    
    plt.xticks(X_axis, categories)
    plt.xlabel('Application category', fontsize=12)
    plt.ylabel('Response time (sec)', fontsize=12)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    # plt.xticks(rotation=90)
    plt.legend()
    # plt.rcParams.update({'font.size': 50})
    # plt.legend(bbox_to_anchor=(0.5,0.7), prop={'size': 18})
    plt.legend(loc='upper right', prop={'size': 12})
    fig.set_size_inches(8, 6)
    plt.savefig('C:\\Users\\houss\\Desktop\\phd\\thesis\\exp-figures\\bar_chart_medium_load_sota.pdf', bbox_inches='tight')
    plt.show()



def scatter_plot():
    planiot_medium_load_directory = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\medium-load\\dataset\\'
    
    baseline_file_path = planiot_medium_load_directory + 'metrics_baseline.csv'
    planiot_file_path = planiot_medium_load_directory + 'metrics_planner.csv'
    rl_file_path = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\medium-load\\jsimg\\default-440.jsimg-result.jsim'
    
    # planiot_file_path = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\medium-load\\jsimg\\default-440.jsimg-result.jsim'
    '''BASELINE SCATTER PLOT'''
    get_response_times_per_topic(baseline_file_path)

    fig, ax = plt.subplots(3, 1, sharex=True, figsize=(12, 10), gridspec_kw={'height_ratios': [1,1,2], 'hspace': 0.3})
    plt.subplot(3, 1, 1)
    xlabels = set()

    for topic in resptime_an.keys():
        xlabels.add(topic)
    for topic in resptime_rt.keys():
        xlabels.add(topic)
    for topic in resptime_ts.keys():
        xlabels.add(topic)
    for topic in resptime_vs.keys():
        xlabels.add(topic)
    xlabels = list(xlabels)
    xlabels.remove('topic6')
    human_sort(xlabels)

    #plotting AN values
    i = 0
    for label in xlabels:
        srt = resptime_an[label]
        topicid = label.replace("topic", "")
        for element in srt:
            if i == 0:
                plt.scatter(topicid, element, c='coral', marker="o", s=85, label = 'AN')
                i += 1
            else:
                plt.scatter(topicid, element, marker="o", s=80, c='coral')
     
    #plotting RT values    
    i = 0   
    for label in xlabels:
        srt = resptime_rt[label]
        topicid = label.replace("topic", "")
        for element in srt:
            if i == 0:
                plt.scatter(topicid, element, c='blue', marker="v", s=85, label = 'RT')
                i += 1
            else:
                plt.scatter(topicid, element,  marker="v", s=85, c='blue')
            
    #plotting TS values   
    i = 0    
    for label in xlabels:
        srt = resptime_ts[label]
        topicid = label.replace("topic", "")
        for element in srt:
            if i == 0:
                plt.scatter(topicid, element, c='red', marker=">", s=85, label = 'TS')
                i += 1
            else:
                plt.scatter(topicid, element, marker=">", s=85, c='red')
            
    #plotting VS values  
    i = 0     
    for label in xlabels:
        srt = resptime_vs[label]
        topicid = label.replace("topic", "")
        for element in srt:
            if i == 0:
                plt.scatter(topicid, element, c='green', marker='x', s=85, label = 'ST')
                i += 1
            else:
                plt.scatter(topicid, element, marker='x', s=85, c='green')
    #x = responseTimes_baseline_ordered.keys()
    #y = responseTimes_baseline_ordered.values()
    ##x = responseTimes_validation_ordered.keys()
    ##y = responseTimes_validation_ordered.values()
    #plt.scatter(x, y)
    # plt.legend(loc ='upper right', prop={'size': 14})
    # fig.set_size_inches(8, 6)
    plt.xticks(rotation=90)
    #plt.xlabel('Topic')
    # ax[1].size
    plt.title('No policy', fontsize=12)
    # plt.ylabel('Response time (in s)')
    plt.ylim([0, 1.5])
    plt.yticks(np.arange(0, 1.52, 0.5))
    plt.rcParams.update({'font.size': 12})
    #plt.savefig(directory_path + 'aiplanning/validation/scatter_resptime_baseline.pdf', bbox_inches='tight')
    # plt.show()
    '''RL SCATTER PLOT'''
    get_response_times_per_topic(rl_file_path)

    plt.subplot(3, 1, 2)
    xlabels = set()

    for topic in resptime_an.keys():
        xlabels.add(topic)
    for topic in resptime_rt.keys():
        xlabels.add(topic)
    for topic in resptime_ts.keys():
        xlabels.add(topic)
    for topic in resptime_vs.keys():
        xlabels.add(topic)
    xlabels = list(xlabels)
    xlabels.remove('topic6')
    human_sort(xlabels)

    #plotting AN values
    i = 0
    for label in xlabels:
        srt = resptime_an[label]
        topicid = label.replace("topic", "")
        for element in srt:
            if i == 0:
                plt.scatter(topicid, element, c='coral', marker="o", s=85, label = 'AN')
                i += 1
            else:
                plt.scatter(topicid, element, marker="o", s=80, c='coral')
     
    #plotting RT values    
    i = 0   
    for label in xlabels:
        srt = resptime_rt[label]
        topicid = label.replace("topic", "")
        for element in srt:
            if i == 0:
                plt.scatter(topicid, element, c='blue', marker="v", s=85, label = 'RT')
                i += 1
            else:
                plt.scatter(topicid, element,  marker="v", s=85, c='blue')
            
    #plotting TS values   
    i = 0    
    for label in xlabels:
        srt = resptime_ts[label]
        topicid = label.replace("topic", "")
        for element in srt:
            if i == 0:
                plt.scatter(topicid, element, c='red', marker=">", s=85, label = 'TS')
                i += 1
            else:
                plt.scatter(topicid, element, marker=">", s=85, c='red')
            
    #plotting VS values  
    i = 0     
    for label in xlabels:
        srt = resptime_vs[label]
        topicid = label.replace("topic", "")
        for element in srt:
            if i == 0:
                plt.scatter(topicid, element, c='green', marker='x', s=85, label = 'ST')
                i += 1
            else:
                plt.scatter(topicid, element, marker='x', s=85, c='green')
    #x = responseTimes_baseline_ordered.keys()
    #y = responseTimes_baseline_ordered.values()
    ##x = responseTimes_validation_ordered.keys()
    ##y = responseTimes_validation_ordered.values()
    #plt.scatter(x, y)
    # plt.legend(loc ='upper right', prop={'size': 14})
    plt.xticks(rotation=90)
    #plt.xlabel('Topic')
    # ax[1].size
    plt.title('RL approaches', fontsize=12)
    # plt.ylabel('Response time (in s)')
    plt.ylim([0, 1.5])
    plt.yticks(np.arange(0, 1.52, 0.5))
    plt.rcParams.update({'font.size': 12})
    # plt.figure().set_figheight(10)
    
    '''PlanIoT Scatter Plot'''
    get_response_times_per_topic(planiot_file_path)
    #fig = plt.figure()
    plt.subplot(3, 1, 3)
    xlabels = set()
    for topic in resptime_an.keys():
        xlabels.add(topic)
    for topic in resptime_rt.keys():
        xlabels.add(topic)
    for topic in resptime_ts.keys():
        xlabels.add(topic)
    for topic in resptime_vs.keys():
        xlabels.add(topic)
    xlabels = list(xlabels)
    xlabels.remove('topic6')
    human_sort(xlabels)
    #plotting AN values
    i = 0
    for label in xlabels:
        srt = resptime_an[label]
        topicid = label.replace("topic", "")
        for element in srt:
            if i == 0:
                plt.scatter(topicid, element, c='coral', marker="o", s=85, label = 'AN')
                i += 1
            else:
                plt.scatter(topicid, element, marker="o", s=85, c='coral')
     
    #plotting RT values    
    i = 0   
    for label in xlabels:
        srt = resptime_rt[label]
        topicid = label.replace("topic", "")
        for element in srt:
            if i == 0:
                plt.scatter(topicid, element, c='blue', marker="v",s=85, label = 'RT')
                i += 1
            else:
                plt.scatter(topicid, element,  marker="v", s=85, c='blue')
            
    #plotting TS values   
    i = 0    
    for label in xlabels:
        srt = resptime_ts[label]
        topicid = label.replace("topic", "")
        for element in srt:
            if i == 0:
                plt.scatter(topicid, element, c='red', marker=">", s=85, label = 'TS')
                i += 1
            else:
                plt.scatter(topicid, element, marker=">", s=85, c='red')
            
    #plotting VS values  
    i = 0     
    for label in xlabels:
        srt = resptime_vs[label]
        topicid = label.replace("topic", "")
        print(topicid)
        for element in srt:
            if i == 0:
                plt.scatter(topicid, element, c='green', marker='x', s=85, label = 'ST')
                i += 1
            else:
                plt.scatter(topicid, element, marker='x', s=85, c='green')
    #x = responseTimes_baseline_ordered.keys()
    #y = responseTimes_baseline_ordered.values()
    ##x = responseTimes_validation_ordered.keys()
    ##y = responseTimes_validation_ordered.values()
    #plt.scatter(x, y)
    plt.legend(loc ='upper right', prop={'size':10})
    # fig.set_size_inches(8, 4)
    plt.xticks(rotation=90, fontsize=12)
    plt.title('PlanIoT', fontsize=12)
    plt.xlabel('Topic id', y=0, fontsize=12)
    fig.supylabel('Response time (sec)', x=0.05, fontsize=12)
    plt.ylim([0, 2.7])
    plt.yticks(np.arange(0, 2.55, 0.5))
    plt.savefig('C:\\Users\\houss\\Desktop\\phd\\thesis\\exp-figures\\scatter_resptime_medium-load.pdf', bbox_inches='tight')
    plt.show()
    
    
    
    
def plot_response_time_evolution():
    
    qos_RT = [0.4, 0.4, 0.4, 0.4, 0.4]
    qos_AN = [1000, 1000, 1000, 1000, 1000]
    qos_VS = [2, 2, 2, 2, 2]
    qos_TS = [4, 4, 4, 4, 4]
    # baseline_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\bw250-proc1.6\\default-20subs.csv'
    # baseline_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\bw250-proc1.6\\default-40subs.csv'
    # baseline_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\bw250-proc1.6\\default-60subs.csv'
    # baseline_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\bw250-proc1.6\\default-80subs.csv'
    # baseline_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\bw250-proc1.6\\default-100subs.csv'

    baseline_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\default-20subs-300.jsimg-result.jsim'
    baseline_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\default-40subs-300.jsimg-result.jsim'
    baseline_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\default-60subs-300.jsimg-result.jsim'
    baseline_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\default-80subs-300.jsimg-result.jsim'
    baseline_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\default-100subs-300.jsimg-result.jsim'
    responseTimes_baseline_20subs = list(get_response_times_per_category(baseline_20subs_file))
    responseTimes_baseline_40subs = list(get_response_times_per_category(baseline_40subs_file))
    responseTimes_baseline_60subs = list(get_response_times_per_category(baseline_60subs_file))
    responseTimes_baseline_80subs = list(get_response_times_per_category(baseline_80subs_file))
    responseTimes_baseline_100subs = list(get_response_times_per_category(baseline_100subs_file))
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
    
    planner_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-20subs-300.jsimg-result.jsim'
    planner_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-40subs-300.jsimg-result.jsim'
    planner_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-60subs-300.jsimg-result.jsim'
    planner_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-80subs-300.jsimg-result.jsim'
    planner_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-100subs-300.jsimg-result.jsim'

    # planner_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\20subs\\dataset\\metrics_planner.csv'
    # planner_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\40subs\\dataset\\metrics_plannerConfiguration.csv'
    # planner_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\60subs\\dataset\\metrics_plannerConfiguration.csv'
    # planner_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\80subs\\dataset\\metrics_plannerConfiguration.csv'
    # planner_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\100subs\\dataset\\metrics_plannerConfiguration.csv'
    responseTimes_planner_20subs = list(get_response_times_per_category(planner_20subs_file))
    responseTimes_planner_40subs = list(get_response_times_per_category(planner_40subs_file))
    responseTimes_planner_60subs = list(get_response_times_per_category(planner_60subs_file))
    responseTimes_planner_80subs = list(get_response_times_per_category(planner_80subs_file))
    responseTimes_planner_100subs = list(get_response_times_per_category(planner_100subs_file))
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
    
    
    '''New Approach with RL'''
    new_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-20subs-300.jsimg-result.jsim'
    new_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-40subs-300.jsimg-result.jsim'
    new_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-60subs-300.jsimg-result.jsim'
    new_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-80subs-500.jsimg-result.jsim'
    new_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-100subs-500.jsimg-result.jsim'
    responseTimes_new_20subs = list(get_response_times_per_category(new_20subs_file))
    responseTimes_new_40subs = list(get_response_times_per_category(new_40subs_file))
    responseTimes_new_60subs = list(get_response_times_per_category(new_60subs_file))
    responseTimes_new_80subs = list(get_response_times_per_category(new_80subs_file))
    responseTimes_new_100subs = list(get_response_times_per_category(new_100subs_file))
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
    
    maxmin_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\maxmin-20subs-300.jsimg-result.jsim'
    maxmin_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\maxmin-40subs-300.jsimg-result.jsim'
    maxmin_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\maxmin-60subs-300.jsimg-result.jsim'
    maxmin_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\maxmin-80subs-300.jsimg-result.jsim'
    maxmin_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\\maxmin-100subs-300.jsimg-result.jsim'

    # maxmin_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\20subs\\dataset\\metrics_maxmin.csv'
    # maxmin_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\40subs\\dataset\\metrics_maxmin.csv'
    # maxmin_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\60subs\dataset\\metrics_maxmin.csv'
    # maxmin_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\80subs\\dataset\\metrics_maxmin.csv'
    # maxmin_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\100subs\\dataset\\metrics_maxmin.csv'
    responseTimes_maxmin_20subs = list(get_response_times_per_category(maxmin_20subs_file))
    responseTimes_maxmin_40subs = list(get_response_times_per_category(maxmin_40subs_file))
    responseTimes_maxmin_60subs = list(get_response_times_per_category(maxmin_60subs_file))
    responseTimes_maxmin_80subs = list(get_response_times_per_category(maxmin_80subs_file))
    responseTimes_maxmin_100subs = list(get_response_times_per_category(maxmin_100subs_file))
    
    # print(responseTimes_maxmin_20subs)
    # print(responseTimes_maxmin_40subs)
    # print(responseTimes_maxmin_60subs)
    # print(responseTimes_maxmin_80subs)
    # print(responseTimes_maxmin_100subs)
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
    
    prioTopics_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\prioritizeTopics-20subs-300.jsimg-result.jsim'
    prioTopics_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\prioritizeTopics-40subs-300.jsimg-result.jsim'
    prioTopics_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\prioritizeTopics-60subs-300.jsimg-result.jsim'
    prioTopics_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\prioritizeTopics-80subs-500.jsimg-result.jsim'
    prioTopics_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\prioritizeTopics-100subs-300.jsimg-result.jsim'

    # prioTopics_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\20subs\\dataset\\metrics_prioritizeTopics.csv'
    # prioTopics_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\40subs\\dataset\\metrics_prioritizeTopics.csv'
    # prioTopics_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\60subs\\dataset\\metrics_prioritizeTopics.csv'
    # prioTopics_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\80subs\\dataset\\metrics_prioritizeTopic.csv'
    # prioTopics_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\100subs\\dataset\\metrics_prioritizeTopics.csv'
    responseTimes_prioTopics_20subs = list(get_response_times_per_category(prioTopics_20subs_file))
    responseTimes_prioTopics_40subs = list(get_response_times_per_category(prioTopics_40subs_file))
    responseTimes_prioTopics_60subs = list(get_response_times_per_category(prioTopics_60subs_file))
    responseTimes_prioTopics_80subs = list(get_response_times_per_category(prioTopics_80subs_file))
    responseTimes_prioTopics_100subs = list(get_response_times_per_category(prioTopics_100subs_file))
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
    print(maxmin_RT)
    prioTopics_RT = [prioTopics_20subs_RT, prioTopics_40subs_RT, prioTopics_60subs_RT, prioTopics_80subs_RT, prioTopics_100subs_RT]
    
    baseline_AN = [baseline_20subs_AN, baseline_40subs_AN, baseline_60subs_AN, baseline_80subs_AN, baseline_100subs_AN]
    planner_AN = [planner_20subs_AN, planner_40subs_AN, planner_60subs_AN, planner_80subs_AN, planner_100subs_AN]
    new_AN = [new_20subs_AN, new_40subs_AN, new_60subs_AN, new_80subs_AN, new_100subs_AN]
    maxmin_AN = [maxmin_20subs_AN, maxmin_40subs_AN, maxmin_60subs_AN, maxmin_80subs_AN, maxmin_100subs_AN]
    prioTopics_AN = [prioTopics_20subs_AN, prioTopics_40subs_AN, prioTopics_60subs_AN, prioTopics_80subs_AN, prioTopics_100subs_AN]
    
    baseline_TS = [baseline_20subs_TS, baseline_40subs_TS, baseline_60subs_TS, baseline_80subs_TS, baseline_100subs_TS]
    planner_TS = [planner_20subs_TS, planner_40subs_TS, planner_60subs_TS, planner_80subs_TS, planner_100subs_TS]
    new_TS = [new_20subs_TS, new_40subs_TS, new_60subs_TS, new_80subs_TS, new_100subs_TS]  
    maxmin_TS = [maxmin_20subs_TS, maxmin_40subs_TS, maxmin_60subs_TS, maxmin_80subs_TS, maxmin_100subs_TS]
    prioTopics_TS = [prioTopics_20subs_TS, prioTopics_40subs_TS, prioTopics_60subs_TS, prioTopics_80subs_TS, prioTopics_100subs_TS]
        
    baseline_VS = [baseline_20subs_VS, baseline_40subs_VS, baseline_60subs_VS, baseline_80subs_VS, baseline_100subs_VS]
    planner_VS = [planner_20subs_VS, planner_40subs_VS, planner_60subs_VS, planner_80subs_VS, planner_100subs_VS]
    new_VS = [new_20subs_VS, new_40subs_VS, new_60subs_VS, new_80subs_VS, new_100subs_VS]
    maxmin_VS = [maxmin_20subs_VS, maxmin_40subs_VS, maxmin_60subs_VS, maxmin_80subs_VS, maxmin_100subs_VS]
    prioTopics_VS = [prioTopics_20subs_VS, prioTopics_40subs_VS, prioTopics_60subs_VS, prioTopics_80subs_VS, prioTopics_100subs_VS]
        
    # x_axis = ['20', '40', '60', '80', '100']
    x_axis = [20, 40, 60, 80, 100]
    x = np.array([20, 40, 60, 80, 100])
    fig, ax = plt.subplots(4, 1, sharex=True)
#    fig.suptitle('Vertically stacked subplots')
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
    qos_AN = [1000, 1000, 1000, 1000, 1000]
    qos_VS = [2, 2, 2, 2, 2]
    qos_TS = [4, 4, 4, 4, 4]
    qos_RT_spline = make_interp_spline(x_axis, qos_RT)
    qos_RT_smoothed = qos_RT_spline(X_)
    qos_AN_spline = make_interp_spline(x_axis, qos_AN)
    qos_AN_smoothed = qos_AN_spline(X_)
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
    # plt.plot(X_, maxmin_AN, label='maxmin', color='orange', marker='p')
    plt.plot(X_, prioTopics_AN_smoothed, color='brown', linewidth=3)
    plt.scatter(x, prioTopics_AN, label='topic priorities', color='brown', marker='s', s=90)
    # plt.plot(X_, qos_AN, '--', label='max. resp. time', linewidth=3.0, color='purple')
    plt.title('AN',  y=0.87, fontsize=24)
    plt.axvspan(80, 100, alpha=0.2, color='red', label='overloaded')
    plt.xticks(fontsize=28)
    plt.xticks([20, 40, 60, 80, 100])
#    plt.xlabel('Number of subscriptions')
    # plt.ylim([0, 100])
    # plt.ylabel('Response time (in s)')
    # plt.legend(loc ='upper left', prop={'size': 12})
#    ax[0].plot(X_, qos_RT, '--', label='QoS requirements', linewidth=3.0, color='purple')
#    ax[0, 0].plot.xlabel('label')
    plt.yticks(fontsize=28)
    
    plt.subplot(2, 2, 2)
    plt.plot(X_, baseline_RT_smoothed, color='blue', linewidth=3)
    plt.scatter(x, baseline_RT, label='baseline', color='blue', marker='o', s=90)
    plt.plot(X_, planner_RT_smoothed, color='green', linewidth=3)
    plt.scatter(x, planner_RT, label='PlanIoT', color='green', marker='v', s=90)
    plt.plot(X_, new_RT_smoothed, color='red', linewidth=3)
    plt.scatter(x, new_RT, label='new approach', color='red', marker='P', s=90)
    # plt.plot(X_, maxmin_RT, label='maxmin', color='orange', marker='p')
    plt.plot(X_, prioTopics_RT_smoothed, color='brown', linewidth=3)
    plt.scatter(x, prioTopics_RT, label='topic priorities', color='brown', marker='s', s=90)
    plt.plot(X_, qos_RT_smoothed, '--', label='max. resp. time', linewidth=3.0, color='purple')
    plt.title('RT',  y=0.87, fontsize=24)
    plt.axvspan(80, 100, alpha=0.2, color='red', label='overloaded')
    plt.xticks(fontsize=28)
    plt.xticks([20, 40, 60, 80, 100])
    # plt.ylim([0, 1])
#    plt.xlabel('Number of subscriptions')
    # plt.legend(loc ='upper left', prop={'size': 9})
    # plt.ylabel('Response time (in s)')
#    plt.legend(loc ='upper left', prop={'size': 10})
    plt.yticks(fontsize=28)
     
    plt.subplot(2, 2, 3)
    plt.plot(X_, baseline_TS_smoothed, color='blue', linewidth=3)
    plt.scatter(x, baseline_TS, label='baseline', color='blue', marker='o', s=90)
    plt.plot(X_, planner_TS_smoothed, color='green', linewidth=3)
    plt.scatter(x, planner_TS, label='PlanIoT', color='green', marker='v', s=90)
    plt.plot(X_, new_TS_smoothed, color='red', linewidth=3)
    plt.scatter(x, new_TS, label='new approach', color='red', marker='P', s=90)
    # plt.plot(X_, maxmin_TS, label='maxmin', color='orange', marker='p')
    plt.plot(X_, prioTopics_TS_smoothed, color='brown', linewidth=3)
    plt.scatter(x, prioTopics_TS, label='topic priorities', color='brown', marker='s', s=90)
    plt.plot(X_, qos_TS_smoothed, '--', label='max. resp. time', linewidth=3.0, color='purple')
    plt.title('TS',  y=0.87, fontsize=24)
    plt.axvspan(80, 100, alpha=0.2, color='red', label='overloaded')
    plt.xticks(fontsize=28)
    plt.xticks([20, 40, 60, 80, 100])
    # plt.ylim([0, 4])
    # plt.xlabel('Number of subscriptions')
    # plt.ylabel('Response time (in s)')
#    plt.legend(loc ='upper left', prop={'size': 10})
    plt.xlabel('Number of subscriptions', fontsize=28)
    plt.yticks(fontsize=28)
    plt.ylabel('Response time (sec)', fontsize=28, y=0.9)
    # plt.legend(loc ='upper right', prop={'size': 16})
     
    plt.subplot(2, 2, 4)
    plt.plot(X_, baseline_VS_smoothed, color='blue', linewidth=3)
    plt.scatter(x, baseline_VS, label='no policy', color='blue', marker='o', s=90)
    plt.plot(X_, planner_VS_smoothed, color='green', linewidth=3)
    plt.scatter(x, planner_VS, label='PlanIoT w/o IRM', color='green', marker='v', s=90)
    plt.plot(X_, new_VS_smoothed, color='red', marker='+', linewidth=3)
    plt.scatter(x, new_VS, label='PlanIoT w/ IRM', color='red', marker='P', s=90)
    # plt.plot(X_, maxmin_VS, label='maxmin', color='orange', marker='p')
    plt.plot(X_, prioTopics_VS_smoothed, color='brown', linewidth=3)
    plt.scatter(x, prioTopics_VS, label='topic priorities', color='brown', marker='s', s=90)
    plt.plot(X_, qos_VS_smoothed, '--', label='max. resp. time', linewidth=3.0, color='purple')
    plt.title('ST',  y=0.9, fontsize=24)
    plt.axvspan(80, 100, alpha=0.2, color='red', label='overloaded')
    # plt.ylim([0, 2])
    plt.xlabel('Number of subscriptions', fontsize=28)
    plt.legend(loc ='upper left', prop={'size': 16})
    # plt.ylabel('Response time (in s)')
#    plt.legend(loc ='upper left', prop={'size': 10})
    
    plt.xlabel('Number of subscriptions', fontsize=28)
    plt.xticks(fontsize=28)
    plt.xticks([20, 40, 60, 80, 100])
    plt.yticks(fontsize=28)
    # plt.ylabel('Response time (in s)')
    fig.set_size_inches(18, 10)
    
    # fig.supylabel('Response time (sec)', fontsize=28)
#    plt.legend()
#    fig.set_size_inches(10, 6)
    plt.rcParams.update({'font.size': 14})
    fig.tight_layout(pad=1.0,)
    # fig.supylabel('Response time (sec)')
    plt.savefig('C:\\Users\\houss\\Desktop\\resptime_increasingsubs_new.png', bbox_inches='tight')
    plt.show()    
  
    
  
def plot_response_time_evolution_vertical():
    
    qos_RT = [0.4, 0.4, 0.4, 0.4, 0.4]
    qos_AN = [1000, 1000, 1000, 1000, 1000]
    qos_VS = [2, 2, 2, 2, 2]
    qos_TS = [4, 4, 4, 4, 4]
    # baseline_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\bw250-proc1.6\\default-20subs.csv'
    # baseline_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\bw250-proc1.6\\default-40subs.csv'
    # baseline_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\bw250-proc1.6\\default-60subs.csv'
    # baseline_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\bw250-proc1.6\\default-80subs.csv'
    # baseline_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\bw250-proc1.6\\default-100subs.csv'

    baseline_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\default-20subs-300.jsimg-result.jsim'
    baseline_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\default-40subs-300.jsimg-result.jsim'
    baseline_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\default-60subs-300.jsimg-result.jsim'
    baseline_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\default-80subs-300.jsimg-result.jsim'
    baseline_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\default-100subs-300.jsimg-result.jsim'
    responseTimes_baseline_20subs = list(get_response_times_per_category(baseline_20subs_file))
    responseTimes_baseline_40subs = list(get_response_times_per_category(baseline_40subs_file))
    responseTimes_baseline_60subs = list(get_response_times_per_category(baseline_60subs_file))
    responseTimes_baseline_80subs = list(get_response_times_per_category(baseline_80subs_file))
    responseTimes_baseline_100subs = list(get_response_times_per_category(baseline_100subs_file))
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
    
    planner_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-20subs-300.jsimg-result.jsim'
    planner_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-40subs-300.jsimg-result.jsim'
    planner_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-60subs-300.jsimg-result.jsim'
    planner_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-80subs-300.jsimg-result.jsim'
    planner_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-100subs-300.jsimg-result.jsim'

    # planner_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\20subs\\dataset\\metrics_planner.csv'
    # planner_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\40subs\\dataset\\metrics_plannerConfiguration.csv'
    # planner_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\60subs\\dataset\\metrics_plannerConfiguration.csv'
    # planner_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\80subs\\dataset\\metrics_plannerConfiguration.csv'
    # planner_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\100subs\\dataset\\metrics_plannerConfiguration.csv'
    responseTimes_planner_20subs = list(get_response_times_per_category(planner_20subs_file))
    responseTimes_planner_40subs = list(get_response_times_per_category(planner_40subs_file))
    responseTimes_planner_60subs = list(get_response_times_per_category(planner_60subs_file))
    responseTimes_planner_80subs = list(get_response_times_per_category(planner_80subs_file))
    responseTimes_planner_100subs = list(get_response_times_per_category(planner_100subs_file))
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
    
    
    '''New Approach with RL'''
    new_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-20subs-300.jsimg-result.jsim'
    new_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-40subs-300.jsimg-result.jsim'
    new_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-60subs-300.jsimg-result.jsim'
    new_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-80subs-500.jsimg-result.jsim'
    new_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-100subs-500.jsimg-result.jsim'
    responseTimes_new_20subs = list(get_response_times_per_category(new_20subs_file))
    responseTimes_new_40subs = list(get_response_times_per_category(new_40subs_file))
    responseTimes_new_60subs = list(get_response_times_per_category(new_60subs_file))
    responseTimes_new_80subs = list(get_response_times_per_category(new_80subs_file))
    responseTimes_new_100subs = list(get_response_times_per_category(new_100subs_file))
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
    
    maxmin_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\maxmin-20subs-300.jsimg-result.jsim'
    maxmin_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\maxmin-40subs-300.jsimg-result.jsim'
    maxmin_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\maxmin-60subs-300.jsimg-result.jsim'
    maxmin_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\maxmin-80subs-300.jsimg-result.jsim'
    maxmin_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\\maxmin-100subs-300.jsimg-result.jsim'

    # maxmin_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\20subs\\dataset\\metrics_maxmin.csv'
    # maxmin_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\40subs\\dataset\\metrics_maxmin.csv'
    # maxmin_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\60subs\dataset\\metrics_maxmin.csv'
    # maxmin_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\80subs\\dataset\\metrics_maxmin.csv'
    # maxmin_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\100subs\\dataset\\metrics_maxmin.csv'
    responseTimes_maxmin_20subs = list(get_response_times_per_category(maxmin_20subs_file))
    responseTimes_maxmin_40subs = list(get_response_times_per_category(maxmin_40subs_file))
    responseTimes_maxmin_60subs = list(get_response_times_per_category(maxmin_60subs_file))
    responseTimes_maxmin_80subs = list(get_response_times_per_category(maxmin_80subs_file))
    responseTimes_maxmin_100subs = list(get_response_times_per_category(maxmin_100subs_file))
    
    # print(responseTimes_maxmin_20subs)
    # print(responseTimes_maxmin_40subs)
    # print(responseTimes_maxmin_60subs)
    # print(responseTimes_maxmin_80subs)
    # print(responseTimes_maxmin_100subs)
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
    
    prioTopics_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\prioritizeTopics-20subs-300.jsimg-result.jsim'
    prioTopics_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\prioritizeTopics-40subs-300.jsimg-result.jsim'
    prioTopics_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\prioritizeTopics-60subs-300.jsimg-result.jsim'
    prioTopics_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\prioritizeTopics-80subs-500.jsimg-result.jsim'
    prioTopics_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\prioritizeTopics-100subs-300.jsimg-result.jsim'

    # prioTopics_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\20subs\\dataset\\metrics_prioritizeTopics.csv'
    # prioTopics_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\40subs\\dataset\\metrics_prioritizeTopics.csv'
    # prioTopics_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\60subs\\dataset\\metrics_prioritizeTopics.csv'
    # prioTopics_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\80subs\\dataset\\metrics_prioritizeTopic.csv'
    # prioTopics_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\100subs\\dataset\\metrics_prioritizeTopics.csv'
    responseTimes_prioTopics_20subs = list(get_response_times_per_category(prioTopics_20subs_file))
    responseTimes_prioTopics_40subs = list(get_response_times_per_category(prioTopics_40subs_file))
    responseTimes_prioTopics_60subs = list(get_response_times_per_category(prioTopics_60subs_file))
    responseTimes_prioTopics_80subs = list(get_response_times_per_category(prioTopics_80subs_file))
    responseTimes_prioTopics_100subs = list(get_response_times_per_category(prioTopics_100subs_file))
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
    print(maxmin_RT)
    prioTopics_RT = [prioTopics_20subs_RT, prioTopics_40subs_RT, prioTopics_60subs_RT, prioTopics_80subs_RT, prioTopics_100subs_RT]
    
    baseline_AN = [baseline_20subs_AN, baseline_40subs_AN, baseline_60subs_AN, baseline_80subs_AN, baseline_100subs_AN]
    planner_AN = [planner_20subs_AN, planner_40subs_AN, planner_60subs_AN, planner_80subs_AN, planner_100subs_AN]
    new_AN = [new_20subs_AN, new_40subs_AN, new_60subs_AN, new_80subs_AN, new_100subs_AN]
    maxmin_AN = [maxmin_20subs_AN, maxmin_40subs_AN, maxmin_60subs_AN, maxmin_80subs_AN, maxmin_100subs_AN]
    prioTopics_AN = [prioTopics_20subs_AN, prioTopics_40subs_AN, prioTopics_60subs_AN, prioTopics_80subs_AN, prioTopics_100subs_AN]
    
    baseline_TS = [baseline_20subs_TS, baseline_40subs_TS, baseline_60subs_TS, baseline_80subs_TS, baseline_100subs_TS]
    planner_TS = [planner_20subs_TS, planner_40subs_TS, planner_60subs_TS, planner_80subs_TS, planner_100subs_TS]
    new_TS = [new_20subs_TS, new_40subs_TS, new_60subs_TS, new_80subs_TS, new_100subs_TS]  
    maxmin_TS = [maxmin_20subs_TS, maxmin_40subs_TS, maxmin_60subs_TS, maxmin_80subs_TS, maxmin_100subs_TS]
    prioTopics_TS = [prioTopics_20subs_TS, prioTopics_40subs_TS, prioTopics_60subs_TS, prioTopics_80subs_TS, prioTopics_100subs_TS]
        
    baseline_VS = [baseline_20subs_VS, baseline_40subs_VS, baseline_60subs_VS, baseline_80subs_VS, baseline_100subs_VS]
    planner_VS = [planner_20subs_VS, planner_40subs_VS, planner_60subs_VS, planner_80subs_VS, planner_100subs_VS]
    new_VS = [new_20subs_VS, new_40subs_VS, new_60subs_VS, new_80subs_VS, new_100subs_VS]
    maxmin_VS = [maxmin_20subs_VS, maxmin_40subs_VS, maxmin_60subs_VS, maxmin_80subs_VS, maxmin_100subs_VS]
    prioTopics_VS = [prioTopics_20subs_VS, prioTopics_40subs_VS, prioTopics_60subs_VS, prioTopics_80subs_VS, prioTopics_100subs_VS]
        
    # x_axis = ['20', '40', '60', '80', '100']
    x_axis = [20, 40, 60, 80, 100]
    x = np.array([20, 40, 60, 80, 100])
    fig, ax = plt.subplots(4, 1, sharex=True)
#    fig.suptitle('Vertically stacked subplots')
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
    qos_AN = [1000, 1000, 1000, 1000, 1000]
    qos_VS = [2, 2, 2, 2, 2]
    qos_TS = [4, 4, 4, 4, 4]
    qos_RT_spline = make_interp_spline(x_axis, qos_RT)
    qos_RT_smoothed = qos_RT_spline(X_)
    qos_AN_spline = make_interp_spline(x_axis, qos_AN)
    qos_AN_smoothed = qos_AN_spline(X_)
    qos_TS_spline = make_interp_spline(x_axis, qos_TS)
    qos_TS_smoothed = qos_TS_spline(X_)
    qos_VS_spline = make_interp_spline(x_axis, qos_VS)
    qos_VS_smoothed = qos_VS_spline(X_)
    
    
    plt.subplot(4, 1, 1)
    plt.plot(X_, baseline_AN_smoothed, color='blue', linewidth=3)
    plt.scatter(x, baseline_AN, label='no policy', color='blue', marker='o', s=90)
    plt.plot(X_, planner_AN_smoothed, color='green', linewidth=3)
    plt.scatter(x, planner_AN, label='PlanIoT', color='green', marker='v', s=90)
    plt.plot(X_, new_AN_smoothed, color='red', linewidth=3)
    plt.scatter(x, new_AN, label='PlanIoT with IRM', color='red', marker='P', s=90)
    # plt.plot(X_, maxmin_AN, label='maxmin', color='orange', marker='p')
    plt.plot(X_, prioTopics_AN_smoothed, color='brown', linewidth=3)
    plt.scatter(x, prioTopics_AN, label='topic priorities', color='brown', marker='s', s=90)
    # plt.plot(X_, qos_AN, '--', label='max. resp. time', linewidth=3.0, color='purple')
    plt.title('AN',  y=0.87, fontsize=24)
    plt.axvspan(80, 100, alpha=0.2, color='red', label='overloaded')
    plt.xticks(fontsize=28)
    plt.xticks([20, 40, 60, 80, 100])
    # plt.legend(loc ='upper left', prop={'size': 16})
#    plt.xlabel('Number of subscriptions')
    # plt.ylim([0, 100])
    # plt.ylabel('Response time (in s)')
    # plt.legend(loc ='upper left', prop={'size': 12})
#    ax[0].plot(X_, qos_RT, '--', label='QoS requirements', linewidth=3.0, color='purple')
#    ax[0, 0].plot.xlabel('label')
    plt.yticks(fontsize=28)
    
    plt.subplot(4, 1, 2)
    plt.plot(X_, baseline_RT_smoothed, color='blue', linewidth=3)
    plt.scatter(x, baseline_RT, label='baseline', color='blue', marker='o', s=90)
    plt.plot(X_, planner_RT_smoothed, color='green', linewidth=3)
    plt.scatter(x, planner_RT, label='PlanIoT', color='green', marker='v', s=90)
    plt.plot(X_, new_RT_smoothed, color='red', linewidth=3)
    plt.scatter(x, new_RT, label='new approach', color='red', marker='P', s=90)
    # plt.plot(X_, maxmin_RT, label='maxmin', color='orange', marker='p')
    plt.plot(X_, prioTopics_RT_smoothed, color='brown', linewidth=3)
    plt.scatter(x, prioTopics_RT, label='topic priorities', color='brown', marker='s', s=90)
    plt.plot(X_, qos_RT_smoothed, '--', label='max. resp. time', linewidth=3.0, color='purple')
    plt.title('RT',  y=0.87, fontsize=24)
    plt.axvspan(80, 100, alpha=0.2, color='red', label='overloaded')
    plt.xticks(fontsize=28)
    plt.xticks([20, 40, 60, 80, 100])
    # plt.ylim([0, 1])
#    plt.xlabel('Number of subscriptions')
    # plt.legend(loc ='upper left', prop={'size': 9})
    # plt.ylabel('Response time (in s)')
#    plt.legend(loc ='upper left', prop={'size': 10})
    plt.yticks(fontsize=28)
     
    plt.subplot(4, 1, 3)
    plt.plot(X_, baseline_TS_smoothed, color='blue', linewidth=3)
    plt.scatter(x, baseline_TS, label='baseline', color='blue', marker='o', s=90)
    plt.plot(X_, planner_TS_smoothed, color='green', linewidth=3)
    plt.scatter(x, planner_TS, label='PlanIoT', color='green', marker='v', s=90)
    plt.plot(X_, new_TS_smoothed, color='red', linewidth=3)
    plt.scatter(x, new_TS, label='new approach', color='red', marker='P', s=90)
    # plt.plot(X_, maxmin_TS, label='maxmin', color='orange', marker='p')
    plt.plot(X_, prioTopics_TS_smoothed, color='brown', linewidth=3)
    plt.scatter(x, prioTopics_TS, label='topic priorities', color='brown', marker='s', s=90)
    plt.plot(X_, qos_TS_smoothed, '--', label='max. resp. time', linewidth=3.0, color='purple')
    plt.title('TS',  y=0.87, fontsize=24)
    plt.axvspan(80, 100, alpha=0.2, color='red', label='overloaded')
    plt.xticks(fontsize=28)
    plt.xticks([20, 40, 60, 80, 100])
    # plt.ylim([0, 4])
    # plt.xlabel('Number of subscriptions')
    # plt.ylabel('Response time (in s)')
#    plt.legend(loc ='upper left', prop={'size': 10})
    # plt.xlabel('Number of subscriptions', fontsize=28)
    plt.yticks(fontsize=28)
    plt.ylabel('Response time (sec)', fontsize=28, y=0.9)
    # plt.legend(loc ='upper right', prop={'size': 16})
     
    plt.subplot(4, 1, 4)
    plt.plot(X_, baseline_VS_smoothed, color='blue', linewidth=3)
    plt.scatter(x, baseline_VS, label='no policy', color='blue', marker='o', s=90)
    plt.plot(X_, planner_VS_smoothed, color='green', linewidth=3)
    plt.scatter(x, planner_VS, label='PlanIoT w/o IRM', color='green', marker='v', s=90)
    plt.plot(X_, new_VS_smoothed, color='red', marker='+', linewidth=3)
    plt.scatter(x, new_VS, label='PlanIoT w/ IRM', color='red', marker='P', s=90)
    # plt.plot(X_, maxmin_VS, label='maxmin', color='orange', marker='p')
    plt.plot(X_, prioTopics_VS_smoothed, color='brown', linewidth=3)
    plt.scatter(x, prioTopics_VS, label='topic priorities', color='brown', marker='s', s=90)
    plt.plot(X_, qos_VS_smoothed, '--', label='max. resp. time', linewidth=3.0, color='purple')
    plt.title('ST',  y=0.9, fontsize=24)
    plt.axvspan(80, 100, alpha=0.2, color='red', label='overloaded')
    # plt.ylim([0, 2])
    # plt.xlabel('Number of subscriptions', fontsize=28)
    # plt.legend(loc ='upper left', prop={'size': 16})
    # plt.ylabel('Response time (in s)')
#    plt.legend(loc ='upper left', prop={'size': 10})
    
    plt.xlabel('Number of subscriptions', fontsize=28)
    plt.xticks(fontsize=28)
    plt.xticks([20, 40, 60, 80, 100])
    plt.yticks(fontsize=28)
    # plt.ylabel('Response time (in s)')
    fig.set_size_inches(12, 18)
    
    # fig.supylabel('Response time (sec)', fontsize=28)
#    plt.legend()
#    fig.set_size_inches(10, 6)
    plt.rcParams.update({'font.size': 14})
    fig.tight_layout(pad=1.0,)
    # fig.supylabel('Response time (sec)')
    plt.savefig('C:\\Users\\houss\\Desktop\\phd\\thesis\\presentation\\figures\\resptime_increasingsubs_new.png', bbox_inches='tight')
    plt.show()    
  
    
def plot_throughput_evolution():
    
    qos_RT = [0.4, 0.4, 0.4, 0.4, 0.4]
    qos_AN = [1000, 1000, 1000, 1000, 1000]
    qos_VS = [2, 2, 2, 2, 2]
    qos_TS = [4, 4, 4, 4, 4]
    # baseline_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\bw250-proc1.6\\default-20subs.csv'
    # baseline_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\bw250-proc1.6\\default-40subs.csv'
    # baseline_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\bw250-proc1.6\\default-60subs.csv'
    # baseline_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\bw250-proc1.6\\default-80subs.csv'
    # baseline_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\bw250-proc1.6\\default-100subs.csv'

    baseline_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\default-20subs-300.jsimg-result.jsim'
    baseline_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\default-40subs-300.jsimg-result.jsim'
    baseline_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\default-60subs-300.jsimg-result.jsim'
    baseline_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\default-80subs-300.jsimg-result.jsim'
    baseline_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\default-100subs-300.jsimg-result.jsim'
    responseTimes_baseline_20subs = list(get_throughput_per_category(baseline_20subs_file))
    responseTimes_baseline_40subs = list(get_throughput_per_category(baseline_40subs_file))
    responseTimes_baseline_60subs = list(get_throughput_per_category(baseline_60subs_file))
    responseTimes_baseline_80subs = list(get_throughput_per_category(baseline_80subs_file))
    responseTimes_baseline_100subs = list(get_throughput_per_category(baseline_100subs_file))
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
    
    planner_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-20subs-300.jsimg-result.jsim'
    planner_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-40subs-300.jsimg-result.jsim'
    planner_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-60subs-300.jsimg-result.jsim'
    planner_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-80subs-300.jsimg-result.jsim'
    planner_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-100subs-300.jsimg-result.jsim'

    # planner_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\20subs\\dataset\\metrics_planner.csv'
    # planner_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\40subs\\dataset\\metrics_plannerConfiguration.csv'
    # planner_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\60subs\\dataset\\metrics_plannerConfiguration.csv'
    # planner_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\80subs\\dataset\\metrics_plannerConfiguration.csv'
    # planner_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\100subs\\dataset\\metrics_plannerConfiguration.csv'
    responseTimes_planner_20subs = list(get_throughput_per_category(planner_20subs_file))
    responseTimes_planner_40subs = list(get_throughput_per_category(planner_40subs_file))
    responseTimes_planner_60subs = list(get_throughput_per_category(planner_60subs_file))
    responseTimes_planner_80subs = list(get_throughput_per_category(planner_80subs_file))
    responseTimes_planner_100subs = list(get_throughput_per_category(planner_100subs_file))
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
    
    
    '''New Approach with RL'''
    new_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-20subs-300.jsimg-result.jsim'
    new_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-40subs-300.jsimg-result.jsim'
    new_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-60subs-300.jsimg-result.jsim'
    new_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-80subs-500.jsimg-result.jsim'
    new_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-100subs-500.jsimg-result.jsim'
    responseTimes_new_20subs = list(get_throughput_per_category(new_20subs_file))
    responseTimes_new_40subs = list(get_throughput_per_category(new_40subs_file))
    responseTimes_new_60subs = list(get_throughput_per_category(new_60subs_file))
    responseTimes_new_80subs = list(get_throughput_per_category(new_80subs_file))
    responseTimes_new_100subs = list(get_throughput_per_category(new_100subs_file))
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
    
    maxmin_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\maxmin-20subs-300.jsimg-result.jsim'
    maxmin_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\maxmin-40subs-300.jsimg-result.jsim'
    maxmin_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\maxmin-60subs-300.jsimg-result.jsim'
    maxmin_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\maxmin-80subs-300.jsimg-result.jsim'
    maxmin_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\\maxmin-100subs-300.jsimg-result.jsim'

    # maxmin_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\20subs\\dataset\\metrics_maxmin.csv'
    # maxmin_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\40subs\\dataset\\metrics_maxmin.csv'
    # maxmin_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\60subs\dataset\\metrics_maxmin.csv'
    # maxmin_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\80subs\\dataset\\metrics_maxmin.csv'
    # maxmin_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\100subs\\dataset\\metrics_maxmin.csv'
    responseTimes_maxmin_20subs = list(get_throughput_per_category(maxmin_20subs_file))
    responseTimes_maxmin_40subs = list(get_throughput_per_category(maxmin_40subs_file))
    responseTimes_maxmin_60subs = list(get_throughput_per_category(maxmin_60subs_file))
    responseTimes_maxmin_80subs = list(get_throughput_per_category(maxmin_80subs_file))
    responseTimes_maxmin_100subs = list(get_throughput_per_category(maxmin_100subs_file))
    
    # print(responseTimes_maxmin_20subs)
    # print(responseTimes_maxmin_40subs)
    # print(responseTimes_maxmin_60subs)
    # print(responseTimes_maxmin_80subs)
    # print(responseTimes_maxmin_100subs)
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
    
    prioTopics_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\prioritizeTopics-20subs-300.jsimg-result.jsim'
    prioTopics_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\prioritizeTopics-40subs-300.jsimg-result.jsim'
    prioTopics_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\prioritizeTopics-60subs-300.jsimg-result.jsim'
    prioTopics_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\prioritizeTopics-80subs-500.jsimg-result.jsim'
    prioTopics_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\prioritizeTopics-100subs-300.jsimg-result.jsim'

    # prioTopics_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\20subs\\dataset\\metrics_prioritizeTopics.csv'
    # prioTopics_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\40subs\\dataset\\metrics_prioritizeTopics.csv'
    # prioTopics_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\60subs\\dataset\\metrics_prioritizeTopics.csv'
    # prioTopics_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\80subs\\dataset\\metrics_prioritizeTopic.csv'
    # prioTopics_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\100subs\\dataset\\metrics_prioritizeTopics.csv'
    responseTimes_prioTopics_20subs = list(get_throughput_per_category(prioTopics_20subs_file))
    responseTimes_prioTopics_40subs = list(get_throughput_per_category(prioTopics_40subs_file))
    responseTimes_prioTopics_60subs = list(get_throughput_per_category(prioTopics_60subs_file))
    responseTimes_prioTopics_80subs = list(get_throughput_per_category(prioTopics_80subs_file))
    responseTimes_prioTopics_100subs = list(get_throughput_per_category(prioTopics_100subs_file))
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
    print(maxmin_RT)
    prioTopics_RT = [prioTopics_20subs_RT, prioTopics_40subs_RT, prioTopics_60subs_RT, prioTopics_80subs_RT, prioTopics_100subs_RT]
    
    baseline_AN = [baseline_20subs_AN, baseline_40subs_AN, baseline_60subs_AN, baseline_80subs_AN, baseline_100subs_AN]
    planner_AN = [planner_20subs_AN, planner_40subs_AN, planner_60subs_AN, planner_80subs_AN, planner_100subs_AN]
    new_AN = [new_20subs_AN, new_40subs_AN, new_60subs_AN, new_80subs_AN, new_100subs_AN]
    maxmin_AN = [maxmin_20subs_AN, maxmin_40subs_AN, maxmin_60subs_AN, maxmin_80subs_AN, maxmin_100subs_AN]
    prioTopics_AN = [prioTopics_20subs_AN, prioTopics_40subs_AN, prioTopics_60subs_AN, prioTopics_80subs_AN, prioTopics_100subs_AN]
    
    baseline_TS = [baseline_20subs_TS, baseline_40subs_TS, baseline_60subs_TS, baseline_80subs_TS, baseline_100subs_TS]
    planner_TS = [planner_20subs_TS, planner_40subs_TS, planner_60subs_TS, planner_80subs_TS, planner_100subs_TS]
    new_TS = [new_20subs_TS, new_40subs_TS, new_60subs_TS, new_80subs_TS, new_100subs_TS]  
    maxmin_TS = [maxmin_20subs_TS, maxmin_40subs_TS, maxmin_60subs_TS, maxmin_80subs_TS, maxmin_100subs_TS]
    prioTopics_TS = [prioTopics_20subs_TS, prioTopics_40subs_TS, prioTopics_60subs_TS, prioTopics_80subs_TS, prioTopics_100subs_TS]
        
    baseline_VS = [baseline_20subs_VS, baseline_40subs_VS, baseline_60subs_VS, baseline_80subs_VS, baseline_100subs_VS]
    planner_VS = [planner_20subs_VS, planner_40subs_VS, planner_60subs_VS, planner_80subs_VS, planner_100subs_VS]
    new_VS = [new_20subs_VS, new_40subs_VS, new_60subs_VS, new_80subs_VS, new_100subs_VS]
    maxmin_VS = [maxmin_20subs_VS, maxmin_40subs_VS, maxmin_60subs_VS, maxmin_80subs_VS, maxmin_100subs_VS]
    prioTopics_VS = [prioTopics_20subs_VS, prioTopics_40subs_VS, prioTopics_60subs_VS, prioTopics_80subs_VS, prioTopics_100subs_VS]
        
    # x_axis = ['20', '40', '60', '80', '100']
    x_axis = [20, 40, 60, 80, 100]
    x = np.array([20, 40, 60, 80, 100])
    fig, ax = plt.subplots(4, 1, sharex=True)
#    fig.suptitle('Vertically stacked subplots')
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
    qos_AN = [1000, 1000, 1000, 1000, 1000]
    qos_VS = [2, 2, 2, 2, 2]
    qos_TS = [4, 4, 4, 4, 4]
    qos_RT_spline = make_interp_spline(x_axis, qos_RT)
    qos_RT_smoothed = qos_RT_spline(X_)
    qos_AN_spline = make_interp_spline(x_axis, qos_AN)
    qos_AN_smoothed = qos_AN_spline(X_)
    qos_TS_spline = make_interp_spline(x_axis, qos_TS)
    qos_TS_smoothed = qos_TS_spline(X_)
    qos_VS_spline = make_interp_spline(x_axis, qos_VS)
    qos_VS_smoothed = qos_VS_spline(X_)
    
    
    plt.subplot(2, 2, 1)
    plt.plot(X_, baseline_AN_smoothed, color='blue', linewidth=3)
    plt.scatter(x, baseline_AN, label='no policy', color='blue', marker='o', s=90)
    plt.plot(X_, planner_AN_smoothed, color='green', linewidth=3)
    plt.scatter(x, planner_AN, label='PlanIoT w/o IRM', color='green', marker='v', s=90)
    plt.plot(X_, new_AN_smoothed, color='red', linewidth=3)
    plt.scatter(x, new_AN, label='PlanIoT w/ IRM', color='red', marker='P', s=90)
    # plt.plot(X_, maxmin_AN, label='maxmin', color='orange', marker='p')
    plt.plot(X_, prioTopics_AN_smoothed, color='brown', linewidth=3)
    plt.scatter(x, prioTopics_AN, label='topic priorities', color='brown', marker='s', s=90)
    # plt.plot(X_, qos_AN, '--', label='max. resp. time', linewidth=3.0, color='purple')
    plt.title('AN',  y=0.87, fontsize=24)
    plt.axvspan(80, 100, alpha=0.2, color='red', label='overloaded')
    plt.xticks(fontsize=28)
    plt.xticks([20, 40, 60, 80, 100])
#    plt.xlabel('Number of subscriptions')
    # plt.ylim([0, 100])
    # plt.ylabel('Response time (in s)')
    # plt.legend(loc ='upper left', prop={'size': 12})
#    ax[0].plot(X_, qos_RT, '--', label='QoS requirements', linewidth=3.0, color='purple')
#    ax[0, 0].plot.xlabel('label')
    plt.yticks(fontsize=28)
    
    
    plt.subplot(2, 2, 2)
    plt.plot(X_, baseline_RT_smoothed, color='blue', linewidth=3)
    plt.scatter(x, baseline_RT, label='baseline', color='blue', marker='o', s=90)
    plt.plot(X_, planner_RT_smoothed, color='green', linewidth=3)
    plt.scatter(x, planner_RT, label='PlanIoT', color='green', marker='v', s=90)
    plt.plot(X_, new_RT_smoothed, color='red', linewidth=3)
    plt.scatter(x, new_RT, label='new approach', color='red', marker='P', s=90)
    # plt.plot(X_, maxmin_RT, label='maxmin', color='orange', marker='p')
    plt.plot(X_, prioTopics_RT_smoothed, color='brown', linewidth=3)
    plt.scatter(x, prioTopics_RT, label='topic priorities', color='brown', marker='s', s=90)
    # plt.plot(X_, qos_RT_smoothed, '--', label='max. resp. time', linewidth=3.0, color='purple')
    plt.title('RT',  y=0.87, fontsize=24)
    plt.axvspan(80, 100, alpha=0.2, color='red', label='overloaded')
    plt.xticks(fontsize=28)
    plt.xticks([20, 40, 60, 80, 100])
    # plt.ylim([0, 1])
#    plt.xlabel('Number of subscriptions')
    # plt.legend(loc ='upper left', prop={'size': 9})
    # plt.ylabel('Response time (in s)')
#    plt.legend(loc ='upper left', prop={'size': 10})
    plt.yticks(fontsize=28)
     
    plt.subplot(2, 2, 3)
    plt.plot(X_, baseline_TS_smoothed, color='blue', linewidth=3)
    plt.scatter(x, baseline_TS, label='baseline', color='blue', marker='o', s=90)
    plt.plot(X_, planner_TS_smoothed, color='green', linewidth=3)
    plt.scatter(x, planner_TS, label='PlanIoT', color='green', marker='v', s=90)
    plt.plot(X_, new_TS_smoothed, color='red', linewidth=3)
    plt.scatter(x, new_TS, label='new approach', color='red', marker='P', s=90)
    # plt.plot(X_, maxmin_TS, label='maxmin', color='orange', marker='p')
    plt.plot(X_, prioTopics_TS_smoothed, color='brown', linewidth=3)
    plt.scatter(x, prioTopics_TS, label='topic priorities', color='brown', marker='s', s=90)
    # plt.plot(X_, qos_TS_smoothed, '--', label='max. resp. time', linewidth=3.0, color='purple')
    plt.title('TS',  y=0.87, fontsize=24)
    plt.axvspan(80, 100, alpha=0.2, color='red', label='overloaded')
    plt.xticks(fontsize=28)
    # plt.ylim([0, 4])
    # plt.xlabel('Number of subscriptions')
    # plt.ylabel('Response time (in s)')
#    plt.legend(loc ='upper left', prop={'size': 10})
    plt.xlabel('Number of subscriptions', fontsize=28)
    plt.yticks(fontsize=28)
    plt.xticks([20, 40, 60, 80, 100])
    plt.ylabel('Throughput (Mbps)', fontsize=28, y=0.9)
     
    plt.subplot(2, 2, 4)
    plt.plot(X_, baseline_VS_smoothed, color='blue', linewidth=3)
    plt.scatter(x, baseline_VS, label='no policy', color='blue', marker='o', s=90)
    plt.plot(X_, planner_VS_smoothed, color='green', linewidth=3)
    plt.scatter(x, planner_VS, label='PlanIoT w/o IRM', color='green', marker='v', s=90)
    plt.plot(X_, new_VS_smoothed, color='red', linewidth=3)
    plt.scatter(x, new_VS, label='PlanIoT w/ IRM', color='red', marker='P', s=90)
    # plt.plot(X_, maxmin_VS, label='maxmin', color='orange', marker='p')
    plt.plot(X_, prioTopics_VS_smoothed, color='brown', linewidth=3)
    plt.scatter(x, prioTopics_VS, label='topic priorities', color='brown', marker='s', s=90)
    # plt.plot(X_, qos_VS_smoothed, '--', label='max. resp. time', linewidth=3.0, color='purple')
    plt.title('ST',  y=0.87, fontsize=24)
    plt.axvspan(80, 100, alpha=0.2, color='red', label='overloaded')
    # plt.ylim([0, 2])
    plt.xlabel('Number of subscriptions', fontsize=28)
    plt.legend(loc ='lower left', prop={'size': 18})
    # plt.ylabel('Response time (in s)')
#    plt.legend(loc ='upper left', prop={'size': 10})
    
    plt.xlabel('Number of subscriptions', fontsize=28)
    plt.xticks(fontsize=28)
    plt.xticks([20, 40, 60, 80, 100])
    plt.yticks(fontsize=28)
    # plt.ylabel('Response time (in s)')
    fig.set_size_inches(24, 10)
    
    # fig.supylabel('Response time (sec)', fontsize=28)
#    plt.legend()
#    fig.set_size_inches(10, 6)
    plt.rcParams.update({'font.size': 14})
    fig.tight_layout(pad=1.0,)
    # fig.supylabel('Response time (sec)')
    plt.savefig('C:\\Users\\houss\\Desktop\\phd\\thesis\\exp-figures\\throughput_increasingsubs_new.pdf', bbox_inches='tight')
    plt.show()    
    
   
    
def plot_throughput_evolution_vertical():
    
    qos_RT = [0.4, 0.4, 0.4, 0.4, 0.4]
    qos_AN = [1000, 1000, 1000, 1000, 1000]
    qos_VS = [2, 2, 2, 2, 2]
    qos_TS = [4, 4, 4, 4, 4]
    # baseline_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\bw250-proc1.6\\default-20subs.csv'
    # baseline_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\bw250-proc1.6\\default-40subs.csv'
    # baseline_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\bw250-proc1.6\\default-60subs.csv'
    # baseline_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\bw250-proc1.6\\default-80subs.csv'
    # baseline_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\bw250-proc1.6\\default-100subs.csv'

    baseline_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\default-20subs-300.jsimg-result.jsim'
    baseline_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\default-40subs-300.jsimg-result.jsim'
    baseline_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\default-60subs-300.jsimg-result.jsim'
    baseline_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\default-80subs-300.jsimg-result.jsim'
    baseline_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\default-100subs-300.jsimg-result.jsim'
    responseTimes_baseline_20subs = list(get_throughput_per_category(baseline_20subs_file))
    responseTimes_baseline_40subs = list(get_throughput_per_category(baseline_40subs_file))
    responseTimes_baseline_60subs = list(get_throughput_per_category(baseline_60subs_file))
    responseTimes_baseline_80subs = list(get_throughput_per_category(baseline_80subs_file))
    responseTimes_baseline_100subs = list(get_throughput_per_category(baseline_100subs_file))
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
    
    planner_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-20subs-300.jsimg-result.jsim'
    planner_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-40subs-300.jsimg-result.jsim'
    planner_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-60subs-300.jsimg-result.jsim'
    planner_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-80subs-300.jsimg-result.jsim'
    planner_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-100subs-300.jsimg-result.jsim'

    # planner_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\20subs\\dataset\\metrics_planner.csv'
    # planner_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\40subs\\dataset\\metrics_plannerConfiguration.csv'
    # planner_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\60subs\\dataset\\metrics_plannerConfiguration.csv'
    # planner_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\80subs\\dataset\\metrics_plannerConfiguration.csv'
    # planner_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\100subs\\dataset\\metrics_plannerConfiguration.csv'
    responseTimes_planner_20subs = list(get_throughput_per_category(planner_20subs_file))
    responseTimes_planner_40subs = list(get_throughput_per_category(planner_40subs_file))
    responseTimes_planner_60subs = list(get_throughput_per_category(planner_60subs_file))
    responseTimes_planner_80subs = list(get_throughput_per_category(planner_80subs_file))
    responseTimes_planner_100subs = list(get_throughput_per_category(planner_100subs_file))
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
    
    
    '''New Approach with RL'''
    new_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-20subs-300.jsimg-result.jsim'
    new_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-40subs-300.jsimg-result.jsim'
    new_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-60subs-300.jsimg-result.jsim'
    new_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-80subs-500.jsimg-result.jsim'
    new_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-100subs-500.jsimg-result.jsim'
    responseTimes_new_20subs = list(get_throughput_per_category(new_20subs_file))
    responseTimes_new_40subs = list(get_throughput_per_category(new_40subs_file))
    responseTimes_new_60subs = list(get_throughput_per_category(new_60subs_file))
    responseTimes_new_80subs = list(get_throughput_per_category(new_80subs_file))
    responseTimes_new_100subs = list(get_throughput_per_category(new_100subs_file))
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
    
    maxmin_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\maxmin-20subs-300.jsimg-result.jsim'
    maxmin_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\maxmin-40subs-300.jsimg-result.jsim'
    maxmin_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\maxmin-60subs-300.jsimg-result.jsim'
    maxmin_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\maxmin-80subs-300.jsimg-result.jsim'
    maxmin_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\\maxmin-100subs-300.jsimg-result.jsim'

    # maxmin_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\20subs\\dataset\\metrics_maxmin.csv'
    # maxmin_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\40subs\\dataset\\metrics_maxmin.csv'
    # maxmin_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\60subs\dataset\\metrics_maxmin.csv'
    # maxmin_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\80subs\\dataset\\metrics_maxmin.csv'
    # maxmin_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\100subs\\dataset\\metrics_maxmin.csv'
    responseTimes_maxmin_20subs = list(get_throughput_per_category(maxmin_20subs_file))
    responseTimes_maxmin_40subs = list(get_throughput_per_category(maxmin_40subs_file))
    responseTimes_maxmin_60subs = list(get_throughput_per_category(maxmin_60subs_file))
    responseTimes_maxmin_80subs = list(get_throughput_per_category(maxmin_80subs_file))
    responseTimes_maxmin_100subs = list(get_throughput_per_category(maxmin_100subs_file))
    
    # print(responseTimes_maxmin_20subs)
    # print(responseTimes_maxmin_40subs)
    # print(responseTimes_maxmin_60subs)
    # print(responseTimes_maxmin_80subs)
    # print(responseTimes_maxmin_100subs)
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
    
    prioTopics_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\prioritizeTopics-20subs-300.jsimg-result.jsim'
    prioTopics_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\prioritizeTopics-40subs-300.jsimg-result.jsim'
    prioTopics_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\prioritizeTopics-60subs-300.jsimg-result.jsim'
    prioTopics_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\prioritizeTopics-80subs-500.jsimg-result.jsim'
    prioTopics_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\prioritizeTopics-100subs-300.jsimg-result.jsim'

    # prioTopics_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\20subs\\dataset\\metrics_prioritizeTopics.csv'
    # prioTopics_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\40subs\\dataset\\metrics_prioritizeTopics.csv'
    # prioTopics_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\60subs\\dataset\\metrics_prioritizeTopics.csv'
    # prioTopics_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\80subs\\dataset\\metrics_prioritizeTopic.csv'
    # prioTopics_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\100subs\\dataset\\metrics_prioritizeTopics.csv'
    responseTimes_prioTopics_20subs = list(get_throughput_per_category(prioTopics_20subs_file))
    responseTimes_prioTopics_40subs = list(get_throughput_per_category(prioTopics_40subs_file))
    responseTimes_prioTopics_60subs = list(get_throughput_per_category(prioTopics_60subs_file))
    responseTimes_prioTopics_80subs = list(get_throughput_per_category(prioTopics_80subs_file))
    responseTimes_prioTopics_100subs = list(get_throughput_per_category(prioTopics_100subs_file))
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
    print(maxmin_RT)
    prioTopics_RT = [prioTopics_20subs_RT, prioTopics_40subs_RT, prioTopics_60subs_RT, prioTopics_80subs_RT, prioTopics_100subs_RT]
    
    baseline_AN = [baseline_20subs_AN, baseline_40subs_AN, baseline_60subs_AN, baseline_80subs_AN, baseline_100subs_AN]
    planner_AN = [planner_20subs_AN, planner_40subs_AN, planner_60subs_AN, planner_80subs_AN, planner_100subs_AN]
    new_AN = [new_20subs_AN, new_40subs_AN, new_60subs_AN, new_80subs_AN, new_100subs_AN]
    maxmin_AN = [maxmin_20subs_AN, maxmin_40subs_AN, maxmin_60subs_AN, maxmin_80subs_AN, maxmin_100subs_AN]
    prioTopics_AN = [prioTopics_20subs_AN, prioTopics_40subs_AN, prioTopics_60subs_AN, prioTopics_80subs_AN, prioTopics_100subs_AN]
    
    baseline_TS = [baseline_20subs_TS, baseline_40subs_TS, baseline_60subs_TS, baseline_80subs_TS, baseline_100subs_TS]
    planner_TS = [planner_20subs_TS, planner_40subs_TS, planner_60subs_TS, planner_80subs_TS, planner_100subs_TS]
    new_TS = [new_20subs_TS, new_40subs_TS, new_60subs_TS, new_80subs_TS, new_100subs_TS]  
    maxmin_TS = [maxmin_20subs_TS, maxmin_40subs_TS, maxmin_60subs_TS, maxmin_80subs_TS, maxmin_100subs_TS]
    prioTopics_TS = [prioTopics_20subs_TS, prioTopics_40subs_TS, prioTopics_60subs_TS, prioTopics_80subs_TS, prioTopics_100subs_TS]
        
    baseline_VS = [baseline_20subs_VS, baseline_40subs_VS, baseline_60subs_VS, baseline_80subs_VS, baseline_100subs_VS]
    planner_VS = [planner_20subs_VS, planner_40subs_VS, planner_60subs_VS, planner_80subs_VS, planner_100subs_VS]
    new_VS = [new_20subs_VS, new_40subs_VS, new_60subs_VS, new_80subs_VS, new_100subs_VS]
    maxmin_VS = [maxmin_20subs_VS, maxmin_40subs_VS, maxmin_60subs_VS, maxmin_80subs_VS, maxmin_100subs_VS]
    prioTopics_VS = [prioTopics_20subs_VS, prioTopics_40subs_VS, prioTopics_60subs_VS, prioTopics_80subs_VS, prioTopics_100subs_VS]
        
    # x_axis = ['20', '40', '60', '80', '100']
    x_axis = [20, 40, 60, 80, 100]
    x = np.array([20, 40, 60, 80, 100])
    fig, ax = plt.subplots(4, 1, sharex=True)
#    fig.suptitle('Vertically stacked subplots')
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
    qos_AN = [1000, 1000, 1000, 1000, 1000]
    qos_VS = [2, 2, 2, 2, 2]
    qos_TS = [4, 4, 4, 4, 4]
    qos_RT_spline = make_interp_spline(x_axis, qos_RT)
    qos_RT_smoothed = qos_RT_spline(X_)
    qos_AN_spline = make_interp_spline(x_axis, qos_AN)
    qos_AN_smoothed = qos_AN_spline(X_)
    qos_TS_spline = make_interp_spline(x_axis, qos_TS)
    qos_TS_smoothed = qos_TS_spline(X_)
    qos_VS_spline = make_interp_spline(x_axis, qos_VS)
    qos_VS_smoothed = qos_VS_spline(X_)
    
    
    plt.subplot(4, 1, 1)
    plt.plot(X_, baseline_AN_smoothed, color='blue', linewidth=3)
    plt.scatter(x, baseline_AN, label='no policy', color='blue', marker='o', s=90)
    plt.plot(X_, planner_AN_smoothed, color='green', linewidth=3)
    plt.scatter(x, planner_AN, label='PlanIoT w/o IRM', color='green', marker='v', s=90)
    plt.plot(X_, new_AN_smoothed, color='red', linewidth=3)
    plt.scatter(x, new_AN, label='PlanIoT w/ IRM', color='red', marker='P', s=90)
    # plt.plot(X_, maxmin_AN, label='maxmin', color='orange', marker='p')
    plt.plot(X_, prioTopics_AN_smoothed, color='brown', linewidth=3)
    plt.scatter(x, prioTopics_AN, label='topic priorities', color='brown', marker='s', s=90)
    # plt.plot(X_, qos_AN, '--', label='max. resp. time', linewidth=3.0, color='purple')
    plt.title('AN',  y=0.87, fontsize=24)
    plt.axvspan(80, 100, alpha=0.2, color='red', label='overloaded')
    plt.xticks(fontsize=28)
    plt.xticks([20, 40, 60, 80, 100])
    # plt.legend(loc ='lower left', prop={'size': 18})
#    plt.xlabel('Number of subscriptions')
    # plt.ylim([0, 100])
    # plt.ylabel('Response time (in s)')
    # plt.legend(loc ='upper left', prop={'size': 12})
#    ax[0].plot(X_, qos_RT, '--', label='QoS requirements', linewidth=3.0, color='purple')
#    ax[0, 0].plot.xlabel('label')
    plt.yticks(fontsize=28)
    
    
    plt.subplot(4, 1, 2)
    plt.plot(X_, baseline_RT_smoothed, color='blue', linewidth=3)
    plt.scatter(x, baseline_RT, label='baseline', color='blue', marker='o', s=90)
    plt.plot(X_, planner_RT_smoothed, color='green', linewidth=3)
    plt.scatter(x, planner_RT, label='PlanIoT', color='green', marker='v', s=90)
    plt.plot(X_, new_RT_smoothed, color='red', linewidth=3)
    plt.scatter(x, new_RT, label='new approach', color='red', marker='P', s=90)
    # plt.plot(X_, maxmin_RT, label='maxmin', color='orange', marker='p')
    plt.plot(X_, prioTopics_RT_smoothed, color='brown', linewidth=3)
    plt.scatter(x, prioTopics_RT, label='topic priorities', color='brown', marker='s', s=90)
    # plt.plot(X_, qos_RT_smoothed, '--', label='max. resp. time', linewidth=3.0, color='purple')
    plt.title('RT',  y=0.87, fontsize=24)
    plt.axvspan(80, 100, alpha=0.2, color='red', label='overloaded')
    plt.xticks(fontsize=28)
    plt.xticks([20, 40, 60, 80, 100])
    # plt.ylim([0, 1])
#    plt.xlabel('Number of subscriptions')
    # plt.legend(loc ='upper left', prop={'size': 9})
    # plt.legend(loc ='lower left', prop={'size': 18})
    # plt.ylabel('Response time (in s)')
#    plt.legend(loc ='upper left', prop={'size': 10})
    plt.yticks(fontsize=28)
     
    plt.subplot(4, 1, 3)
    plt.plot(X_, baseline_TS_smoothed, color='blue', linewidth=3)
    plt.scatter(x, baseline_TS, label='baseline', color='blue', marker='o', s=90)
    plt.plot(X_, planner_TS_smoothed, color='green', linewidth=3)
    plt.scatter(x, planner_TS, label='PlanIoT', color='green', marker='v', s=90)
    plt.plot(X_, new_TS_smoothed, color='red', linewidth=3)
    plt.scatter(x, new_TS, label='new approach', color='red', marker='P', s=90)
    # plt.plot(X_, maxmin_TS, label='maxmin', color='orange', marker='p')
    plt.plot(X_, prioTopics_TS_smoothed, color='brown', linewidth=3)
    plt.scatter(x, prioTopics_TS, label='topic priorities', color='brown', marker='s', s=90)
    # plt.plot(X_, qos_TS_smoothed, '--', label='max. resp. time', linewidth=3.0, color='purple')
    plt.title('TS',  y=0.87, fontsize=24)
    plt.axvspan(80, 100, alpha=0.2, color='red', label='overloaded')
    plt.xticks(fontsize=28)
    # plt.ylim([0, 4])
    # plt.xlabel('Number of subscriptions')
    # plt.ylabel('Response time (in s)')
#    plt.legend(loc ='upper left', prop={'size': 10})
    # plt.xlabel('Number of subscriptions', fontsize=28)
    plt.yticks(fontsize=28)
    plt.xticks([20, 40, 60, 80, 100])
    plt.ylabel('Throughput (Mbps)', fontsize=28, y=0.9)
     
    plt.subplot(4, 1, 4)
    plt.plot(X_, baseline_VS_smoothed, color='blue', linewidth=3)
    plt.scatter(x, baseline_VS, label='no policy', color='blue', marker='o', s=90)
    plt.plot(X_, planner_VS_smoothed, color='green', linewidth=3)
    plt.scatter(x, planner_VS, label='PlanIoT w/o IRM', color='green', marker='v', s=90)
    plt.plot(X_, new_VS_smoothed, color='red', linewidth=3)
    plt.scatter(x, new_VS, label='PlanIoT w/ IRM', color='red', marker='P', s=90)
    # plt.plot(X_, maxmin_VS, label='maxmin', color='orange', marker='p')
    plt.plot(X_, prioTopics_VS_smoothed, color='brown', linewidth=3)
    plt.scatter(x, prioTopics_VS, label='topic priorities', color='brown', marker='s', s=90)
    # plt.plot(X_, qos_VS_smoothed, '--', label='max. resp. time', linewidth=3.0, color='purple')
    plt.title('ST',  y=0.87, fontsize=24)
    plt.axvspan(80, 100, alpha=0.2, color='red', label='overloaded')
    # plt.ylim([0, 2])
    # plt.xlabel('Number of subscriptions', fontsize=28)
    # plt.legend(loc ='lower left', prop={'size': 18})
    # plt.ylabel('Response time (in s)')
#    plt.legend(loc ='upper left', prop={'size': 10})
    
    plt.xlabel('Number of subscriptions', fontsize=28)
    plt.xticks(fontsize=28)
    plt.xticks([20, 40, 60, 80, 100])
    plt.yticks(fontsize=28)
    # plt.ylabel('Response time (in s)')
    fig.set_size_inches(12, 18)
    
    # fig.supylabel('Response time (sec)', fontsize=28)
#    plt.legend()
#    fig.set_size_inches(10, 6)
    plt.rcParams.update({'font.size': 14})
    fig.tight_layout(pad=1.0,)
    # fig.supylabel('Response time (sec)')
    plt.savefig('C:\\Users\\houss\\Desktop\\phd\\thesis\\presentation\\figures\\throughput_increasingsubs_new.png', bbox_inches='tight')
    plt.show()    
    
def plot_response_time_evolution_zoomed():
    
    qos_RT = [0.4, 0.4, 0.4, 0.4, 0.4]
    qos_AN = [1000, 1000, 1000, 1000, 1000]
    qos_VS = [2, 2, 2, 2, 2]
    qos_TS = [4, 4, 4, 4, 4]
    # baseline_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\bw250-proc1.6\\default-20subs.csv'
    # baseline_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\bw250-proc1.6\\default-40subs.csv'
    # baseline_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\bw250-proc1.6\\default-60subs.csv'
    # baseline_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\bw250-proc1.6\\default-80subs.csv'
    # baseline_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\bw250-proc1.6\\default-100subs.csv'

    baseline_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\default-20subs-300.jsimg-result.jsim'
    baseline_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\default-40subs-300.jsimg-result.jsim'
    baseline_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\default-60subs-300.jsimg-result.jsim'
    baseline_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\default-80subs-300.jsimg-result.jsim'
    baseline_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\default-100subs-300.jsimg-result.jsim'
    responseTimes_baseline_20subs = list(get_response_times_per_category(baseline_20subs_file))
    responseTimes_baseline_40subs = list(get_response_times_per_category(baseline_40subs_file))
    responseTimes_baseline_60subs = list(get_response_times_per_category(baseline_60subs_file))
    responseTimes_baseline_80subs = list(get_response_times_per_category(baseline_80subs_file))
    responseTimes_baseline_100subs = list(get_response_times_per_category(baseline_100subs_file))
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
    
    planner_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-20subs-300.jsimg-result.jsim'
    planner_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-40subs-300.jsimg-result.jsim'
    planner_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-60subs-300.jsimg-result.jsim'
    planner_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-80subs-300.jsimg-result.jsim'
    planner_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-100subs-300.jsimg-result.jsim'

    # planner_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\20subs\\dataset\\metrics_planner.csv'
    # planner_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\40subs\\dataset\\metrics_plannerConfiguration.csv'
    # planner_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\60subs\\dataset\\metrics_plannerConfiguration.csv'
    # planner_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\80subs\\dataset\\metrics_plannerConfiguration.csv'
    # planner_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\100subs\\dataset\\metrics_plannerConfiguration.csv'
    responseTimes_planner_20subs = list(get_response_times_per_category(planner_20subs_file))
    responseTimes_planner_40subs = list(get_response_times_per_category(planner_40subs_file))
    responseTimes_planner_60subs = list(get_response_times_per_category(planner_60subs_file))
    responseTimes_planner_80subs = list(get_response_times_per_category(planner_80subs_file))
    responseTimes_planner_100subs = list(get_response_times_per_category(planner_100subs_file))
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
    
    
    '''New Approach with RL'''
    new_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-20subs-300.jsimg-result.jsim'
    new_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-40subs-300.jsimg-result.jsim'
    new_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-60subs-300.jsimg-result.jsim'
    new_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-80subs-500.jsimg-result.jsim'
    new_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\plannerConfiguration-100subs-500.jsimg-result.jsim'
    responseTimes_new_20subs = list(get_response_times_per_category(new_20subs_file))
    responseTimes_new_40subs = list(get_response_times_per_category(new_40subs_file))
    responseTimes_new_60subs = list(get_response_times_per_category(new_60subs_file))
    responseTimes_new_80subs = list(get_response_times_per_category(new_80subs_file))
    responseTimes_new_100subs = list(get_response_times_per_category(new_100subs_file))
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
    
    maxmin_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\maxmin-20subs-300.jsimg-result.jsim'
    maxmin_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\maxmin-40subs-300.jsimg-result.jsim'
    maxmin_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\maxmin-60subs-300.jsimg-result.jsim'
    maxmin_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\maxmin-80subs-300.jsimg-result.jsim'
    maxmin_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\\maxmin-100subs-300.jsimg-result.jsim'

    # maxmin_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\20subs\\dataset\\metrics_maxmin.csv'
    # maxmin_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\40subs\\dataset\\metrics_maxmin.csv'
    # maxmin_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\60subs\dataset\\metrics_maxmin.csv'
    # maxmin_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\80subs\\dataset\\metrics_maxmin.csv'
    # maxmin_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\100subs\\dataset\\metrics_maxmin.csv'
    responseTimes_maxmin_20subs = list(get_response_times_per_category(maxmin_20subs_file))
    responseTimes_maxmin_40subs = list(get_response_times_per_category(maxmin_40subs_file))
    responseTimes_maxmin_60subs = list(get_response_times_per_category(maxmin_60subs_file))
    responseTimes_maxmin_80subs = list(get_response_times_per_category(maxmin_80subs_file))
    responseTimes_maxmin_100subs = list(get_response_times_per_category(maxmin_100subs_file))
    
    # print(responseTimes_maxmin_20subs)
    # print(responseTimes_maxmin_40subs)
    # print(responseTimes_maxmin_60subs)
    # print(responseTimes_maxmin_80subs)
    # print(responseTimes_maxmin_100subs)
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
    
    prioTopics_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\prioritizeTopics-20subs-300.jsimg-result.jsim'
    prioTopics_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\prioritizeTopics-40subs-300.jsimg-result.jsim'
    prioTopics_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\prioritizeTopics-60subs-300.jsimg-result.jsim'
    prioTopics_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\prioritizeTopics-80subs-300.jsimg-result.jsim'
    prioTopics_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\increasing-subscriptions\\jsimg\\results\\prioritizeTopics-100subs-300.jsimg-result.jsim'

    # prioTopics_20subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\20subs\\dataset\\metrics_prioritizeTopics.csv'
    # prioTopics_40subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\40subs\\dataset\\metrics_prioritizeTopics.csv'
    # prioTopics_60subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\60subs\\dataset\\metrics_prioritizeTopics.csv'
    # prioTopics_80subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\80subs\\dataset\\metrics_prioritizeTopic.csv'
    # prioTopics_100subs_file = 'C:\\Users\\houss\\Desktop\\repos\\planiot\\Scenarios\\increasing-subscriptions\\100subs\\dataset\\metrics_prioritizeTopics.csv'
    responseTimes_prioTopics_20subs = list(get_response_times_per_category(prioTopics_20subs_file))
    responseTimes_prioTopics_40subs = list(get_response_times_per_category(prioTopics_40subs_file))
    responseTimes_prioTopics_60subs = list(get_response_times_per_category(prioTopics_60subs_file))
    responseTimes_prioTopics_80subs = list(get_response_times_per_category(prioTopics_80subs_file))
    responseTimes_prioTopics_100subs = list(get_response_times_per_category(prioTopics_100subs_file))
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
    
    baseline_AN = [baseline_20subs_AN, baseline_40subs_AN, baseline_60subs_AN, baseline_80subs_AN, baseline_100subs_AN]
    planner_AN = [planner_20subs_AN, planner_40subs_AN, planner_60subs_AN, planner_80subs_AN, planner_100subs_AN]
    new_AN = [new_20subs_AN, new_40subs_AN, new_60subs_AN, new_80subs_AN, new_100subs_AN]
    maxmin_AN = [maxmin_20subs_AN, maxmin_40subs_AN, maxmin_60subs_AN, maxmin_80subs_AN, maxmin_100subs_AN]
    prioTopics_AN = [prioTopics_20subs_AN, prioTopics_40subs_AN, prioTopics_60subs_AN, prioTopics_80subs_AN, prioTopics_100subs_AN]
    
    
    baseline_TS = [baseline_20subs_TS, baseline_40subs_TS, baseline_60subs_TS, baseline_80subs_TS, baseline_100subs_TS]
    planner_TS = [planner_20subs_TS, planner_40subs_TS, planner_60subs_TS, planner_80subs_TS, planner_100subs_TS]
    new_TS = [new_20subs_TS, new_40subs_TS, new_60subs_TS, new_80subs_TS, new_100subs_TS]  
    maxmin_TS = [maxmin_20subs_TS, maxmin_40subs_TS, maxmin_60subs_TS, maxmin_80subs_TS, maxmin_100subs_TS]
    prioTopics_TS = [prioTopics_20subs_TS, prioTopics_40subs_TS, prioTopics_60subs_TS, prioTopics_80subs_TS, prioTopics_100subs_TS]
        
    baseline_VS = [baseline_20subs_VS, baseline_40subs_VS, baseline_60subs_VS, baseline_80subs_VS, baseline_100subs_VS]
    planner_VS = [planner_20subs_VS, planner_40subs_VS, planner_60subs_VS, planner_80subs_VS, planner_100subs_VS]
    new_VS = [new_20subs_VS, new_40subs_VS, new_60subs_VS, new_80subs_VS, new_100subs_VS]
    maxmin_VS = [maxmin_20subs_VS, maxmin_40subs_VS, maxmin_60subs_VS, maxmin_80subs_VS, maxmin_100subs_VS]
    prioTopics_VS = [prioTopics_20subs_VS, prioTopics_40subs_VS, prioTopics_60subs_VS, prioTopics_80subs_VS, prioTopics_100subs_VS]
    
    print(planner_AN)
    print(new_AN)
    print(planner_RT)
    print(new_RT)
    print(planner_TS)
    print(new_TS)
    print(planner_VS)
    print(new_VS)
        
    # x_axis = ['20', '40', '60', '80', '100']
    x_axis = [20, 40, 60, 80, 100]
    x = np.array([20, 40, 60, 80, 100])
    fig, ax = plt.subplots(4, 1, sharex=True)
#    fig.suptitle('Vertically stacked subplots')
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
    qos_AN = [1000, 1000, 1000, 1000, 1000]
    qos_VS = [2, 2, 2, 2, 2]
    qos_TS = [4, 4, 4, 4, 4]
    qos_RT_spline = make_interp_spline(x_axis, qos_RT)
    qos_RT_smoothed = qos_RT_spline(X_)
    qos_AN_spline = make_interp_spline(x_axis, qos_AN)
    qos_AN_smoothed = qos_AN_spline(X_)
    qos_TS_spline = make_interp_spline(x_axis, qos_TS)
    qos_TS_smoothed = qos_TS_spline(X_)
    qos_VS_spline = make_interp_spline(x_axis, qos_VS)
    qos_VS_smoothed = qos_VS_spline(X_)
    
    
    plt.subplot(2, 2, 1)
    # plt.plot(X_, baseline_AN_smoothed, color='blue')
    # plt.scatter(x, baseline_AN, label='default', color='blue', marker='o')
    plt.plot(X_, planner_AN_smoothed, color='green')
    plt.scatter(x, planner_AN, label='PlanIoT', color='green', marker='v')
    plt.plot(X_, new_AN_smoothed, color='red')
    plt.scatter(x, new_AN, label='new approach', color='red', marker='+')
    # plt.plot(X_, maxmin_AN, label='maxmin', color='orange', marker='p')
    # plt.plot(X_, prioTopics_AN_smoothed, color='brown')
    # plt.scatter(x, prioTopics_AN, label='topic priorities', color='brown', marker='s')
    # plt.plot(X_, qos_AN, '--', label='max. resp. time', linewidth=3.0, color='purple')
    plt.title('AN',  y=0.87, fontsize=24)
    plt.axvspan(80, 100, alpha=0.2, color='red', label='overloaded')
    plt.xticks(fontsize=28)
#    plt.xlabel('Number of subscriptions')
    # plt.ylim([0, 100])
    # plt.ylabel('Response time (in s)')
    # plt.legend(loc ='upper left', prop={'size': 12})
#    ax[0].plot(X_, qos_RT, '--', label='QoS requirements', linewidth=3.0, color='purple')
#    ax[0, 0].plot.xlabel('label')
    plt.yticks(fontsize=28)
    
    plt.subplot(2, 2, 2)
    # plt.plot(X_, baseline_RT_smoothed, color='blue')
    # plt.scatter(x, baseline_RT, label='baseline', color='blue', marker='o')
    plt.plot(X_, planner_RT_smoothed, color='green')
    plt.scatter(x, planner_RT, label='PlanIoT', color='green', marker='v')
    plt.plot(X_, new_RT_smoothed, color='red')
    plt.scatter(x, new_RT, label='new approach', color='red', marker='+')
    # plt.plot(X_, maxmin_RT, label='maxmin', color='orange', marker='p')
    # plt.plot(X_, prioTopics_RT_smoothed, color='brown')
    # plt.scatter(x, prioTopics_RT, label='topic priorities', color='brown', marker='s')
    plt.plot(X_, qos_RT_smoothed, '--', label='max. resp. time', linewidth=3.0, color='purple')
    plt.title('RT',  y=0.87, fontsize=24)
    plt.axvspan(80, 100, alpha=0.2, color='red', label='overloaded')
    plt.xticks(fontsize=28)
    plt.ylim([0, 1])
#    plt.xlabel('Number of subscriptions')
    # plt.legend(loc ='upper left', prop={'size': 9})
    # plt.ylabel('Response time (in s)')
#    plt.legend(loc ='upper left', prop={'size': 10})
    plt.yticks(fontsize=28)
     
    plt.subplot(2, 2, 3)
    # plt.plot(X_, baseline_TS_smoothed, color='blue')
    # plt.scatter(x, baseline_TS, label='baseline', color='blue', marker='o')
    plt.plot(X_, planner_TS_smoothed, color='green')
    plt.scatter(x, planner_TS, label='PlanIoT', color='green', marker='v')
    plt.plot(X_, new_TS_smoothed, color='red')
    plt.scatter(x, new_TS, label='new approach', color='red', marker='+')
    # plt.plot(X_, maxmin_TS, label='maxmin', color='orange', marker='p')
    # plt.plot(X_, prioTopics_TS_smoothed, color='brown')
    # plt.scatter(x, prioTopics_TS, label='topic priorities', color='brown', marker='s')
    # plt.plot(X_, qos_TS_smoothed, '--', label='max. resp. time', linewidth=3.0, color='purple')
    plt.title('TS',  y=0.87, fontsize=24)
    plt.axvspan(80, 100, alpha=0.2, color='red', label='overloaded')
    plt.xticks(fontsize=28)
    # plt.ylim([0, 4])
    # plt.xlabel('Number of subscriptions')
    # plt.ylabel('Response time (in s)')
#    plt.legend(loc ='upper left', prop={'size': 10})
    plt.xlabel('Number of subscriptions', fontsize=28)
    plt.yticks(fontsize=28)
    plt.ylabel('Response time (sec)', fontsize=28, y=0.9)
     
    plt.subplot(2, 2, 4)
    # plt.plot(X_, baseline_VS_smoothed, color='blue')
    # plt.scatter(x, baseline_VS, label='baseline', color='blue', marker='o')
    plt.plot(X_, planner_VS_smoothed, color='green')
    plt.scatter(x, planner_VS, label='PlanIoT', color='green', marker='v')
    plt.plot(X_, new_VS_smoothed, color='red', marker='+')
    plt.scatter(x, new_VS, label='new approach', color='red', marker='+')
    # plt.plot(X_, maxmin_VS, label='maxmin', color='orange', marker='p')
    # plt.plot(X_, prioTopics_VS_smoothed, color='brown', linewidth=1)
    # plt.scatter(x, prioTopics_VS, label='topic priorities', color='brown', marker='s')
    # plt.plot(X_, qos_VS_smoothed, '--', label='max. resp. time', linewidth=3.0, color='purple')
    plt.title('VS',  y=0.87, fontsize=24)
    plt.axvspan(80, 100, alpha=0.2, color='red', label='overloaded')
    # plt.ylim([0, 2])
    plt.xlabel('Number of subscriptions', fontsize=28)
    plt.legend(loc ='bottom left', prop={'size': 14})
    # plt.ylabel('Response time (in s)')
#    plt.legend(loc ='upper left', prop={'size': 10})
    
    plt.xlabel('Number of subscriptions', fontsize=28)
    plt.xticks(fontsize=28)
    plt.yticks(fontsize=28)
    # plt.ylabel('Response time (in s)')
    fig.set_size_inches(24, 10)
    
    # fig.supylabel('Response time (sec)', fontsize=28)
#    plt.legend()
#    fig.set_size_inches(10, 6)
    plt.rcParams.update({'font.size': 14})
    fig.tight_layout(pad=1.0,)
    # fig.supylabel('Response time (sec)')
    plt.savefig('C:\\Users\\houss\\Desktop\\repos\\taas\\experiments\\figures\\resptime_increasingsubs_zoomed.pdf', bbox_inches='tight')
    plt.show()    
    
    
# bar_chart_medium_load()
# scatter_plot()
# plot_response_time_evolution_vertical()
plot_response_time_evolution()
# plot_throughput_evolution_vertical()
# plot_response_time_evolution_zoomed()