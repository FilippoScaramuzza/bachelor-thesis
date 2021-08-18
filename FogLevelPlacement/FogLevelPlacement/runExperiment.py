#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import placeService
import generateSimulationSummary
import json
import matplotlib.pyplot as plt
import pathlib
import numpy as np

# Erase previus results
file = open('exp_json/placementResults.json', 'w')
file.write("[]")
file.close()

param_to_change = "FUNC_APP_GENERATION"
value_from = 4
value_to = 21
step = 1

for x in range(value_from, value_to, step):
    placeService.run(param_to_change, f'"nx.gn_graph({x})"', x)
    generateSimulationSummary.run("Increasing number of services with fixed global resources.", f"service_num_{x}")

# Data for plotting
t = np.arange(value_from, value_to, step)
path = pathlib.Path("exp_json")
pathplots = pathlib.Path("plots")
s = [v["app_placed"]/v["app_total"] for v in json.loads(open(str(path.absolute()) + "/placementResults.json").read())]

fig, ax = plt.subplots()
ax.plot(t, s, 'ro-')

ax.set(xlabel="Number of services", ylabel='App Placed / Total Apps',
       title='Increasing amount of services with fixed global required resources')
ax.grid()

plt.savefig(str(pathplots.absolute()) + '/placement_success.pdf',format='pdf')
plt.savefig(str(pathplots.absolute()) + '/placement_success.png',format='png')
plt.show()