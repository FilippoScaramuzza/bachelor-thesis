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

PARAM_TO_CHANGE = "FUNC_APP_GENERATION"
VALUE_FROM = 1
VALUE_TO = 25
STEP = 1

for x in range(VALUE_FROM, VALUE_TO, STEP):
    placeService.run(PARAM_TO_CHANGE, f'"nx.gn_graph({x})"', x)
    generateSimulationSummary.run("Increasing number of services with fixed global resources.", f"service_num_{x}")

# Data for plotting
t = np.arange(VALUE_FROM, VALUE_TO, STEP)
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