# -*- coding: utf-8 -*-
"""
Created on Sat Jan 19 20:38:07 2019

@author: Helge
"""

import numpy as np
import matplotlib.pyplot as plt


##########################
# Parameters
##########################

t_high = 10
t_low = 0
q_high = 5
q_low = -5
e_low = 0
e_mid = 5
e_high = 10
E = 100000
K = np.linspace(0, 5, num=11)
number_Ks = len(K)


##########################
# Functions
##########################


def project(q_low, q_high, t_low, t_high):
    value_p = np.random.random() * (q_high - q_low) + q_low
    type_p = np.random.random() * (t_high - t_low) + t_low
    return value_p, type_p


def perceive_quality(value_p, type_p, type_ind):
    # Response == 1: accept
    knowledge_distance = abs(type_p - type_ind)
    noise = np.random.normal(0, knowledge_distance)
    perceive = value_p + noise
    return perceive


def choose_individual(value_p, per_e_mid):
    if per_e_mid > 0:
        performance = value_p
    else:
        performance = 0
    return performance

##########################
# Please change the following functions!
##########################


def choose_delegate(value_p, per_e_low, per_e_mid, per_e_high, type_p,
                    e_low, e_mid, e_high):
    decision = 0
    if type_p < ((e_mid + e_low)/2):
        if per_e_low > 0:
            decision = 1
    elif type_p > ((e_mid + e_high)/2):
        if per_e_high > 0:
            decision = 1
    else:
        if per_e_mid > 0:
            decision = 1
    if decision == 1:
        performance = value_p
    else:
        performance = 0
    return performance


def choose_voting(value_p, per_e_low, per_e_mid, per_e_high):
    vote = 0
    if per_e_low > 0:
        vote += 1
    if per_e_mid > 0:
        vote += 1
    if per_e_high > 0:
        vote += 1
    if vote >= 2:
        performance = value_p
    else:
        performance = 0
    return performance


def choose_average(value_p, per_e_low, per_e_mid, per_e_high):
    per_vector = [per_e_low, per_e_mid, per_e_high]
    decision = np.average(per_vector)
    if decision > 0:
        performance = value_p
    else:
        performance = 0
    return performance


performance_matrix = np.zeros((number_Ks, 4))
temp_matrix = np.zeros((E, 4))
value_type_matrix = np.zeros((E, 2))
# Save each result in matrix
# 0  for individual, 1, for delegating, 2 for voting, 3 for averageing

##########################
# Simulation
##########################

k_counter = 0
for k in K:
    print('At k: ', k)
    e_high = 5 + k
    e_low = 5 - k
    for e in range(E):
        (value_p, type_p) = project(q_low, q_high, t_low, t_high)
        value_type_matrix[e,0] = value_p
        value_type_matrix[e,1] = type_p
        # print('Value: ', value_p, ' and type: ', type_p)
        # Perception by three agents
        per_e_low = perceive_quality(value_p, type_p, e_low)
        per_e_mid = perceive_quality(value_p, type_p, e_mid)
        # print('Individual perception: ', per_e_mid)
        per_e_high = perceive_quality(value_p, type_p, e_high)
        # Individual
        temp_matrix[e,0] = choose_individual(value_p, per_e_mid)
        # print('Ind. performance: ', temp_matrix[e,0])
        temp_matrix[e,1] = choose_delegate(value_p, per_e_low, per_e_mid,
                                           per_e_high, type_p,
                                           e_low, e_mid, e_high)
        temp_matrix[e,2] = choose_voting(value_p, per_e_low, per_e_mid,
                                         per_e_high)
        temp_matrix[e,3] = choose_average(value_p, per_e_low, per_e_mid,
                                          per_e_high)
    # print(temp_matrix[:,0])
    performance_matrix[k_counter, 0] = np.average(temp_matrix[:,0])
    performance_matrix[k_counter, 1] = np.average(temp_matrix[:,1])
    performance_matrix[k_counter, 2] = np.average(temp_matrix[:,2])
    performance_matrix[k_counter, 3] = np.average(temp_matrix[:,3])
    k_counter += 1
    # Test whether correct calculation
    average_value = np.average(value_type_matrix[:,0])
    # print('Average value', average_value)
    average_type = np.average(value_type_matrix[:,1])
    # print('Average type', average_type)

# print(performance_matrix)

##########################
# Figures
##########################

plt.figure(dpi=150)
plt.axes(frameon=0)
plt.grid()
ax = plt.subplot(111)
plt.ylabel('Perfomance')
plt.xlabel('Knowledge breadth')
linestyles = ['-', '--']
markers = ['v', '^', 'o', 's', 'D']

line_no = 0

for x in range(4):
    style = linestyles[(line_no % len(linestyles))]
    marker = markers[(line_no % len(markers))]
    line_no += 1
    if x == 0:
        label='Individual'
    elif x == 1:
        label='Delegation'
    elif x == 2:
        label='Voting'
    elif x == 3:
        label='Averaging'
    # print(round_no)
    # print(VAR_1)
    X = K
    Z = performance_matrix[:,x]
    ax.plot(X, Z, label=label, linestyle=style, marker=marker, markevery=1,
            linewidth=1)

box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width, box.height])
ax.yaxis.grid(which="major", color='lightgray', linewidth=1,
              rasterized=True, markeredgecolor='white')

lgd = ax.legend(loc='best', title='', frameon=True, fancybox=True,
                framealpha=0.75)

name = 'main'
graph_name = name + '.png'
# plt.subplots_adjust(right=1.5)
# sns.despine()
plt.tight_layout()
# plt.savefig(graph_name, format='png', bbox_extra_artists=[lgd])

plt.show()
plt.close()
