import json
import matplotlib.pyplot as plt
import pathlib
import numpy as np

# Data for plotting
t = np.arange(0, 101, 5)
path = pathlib.Path("exp_json")
pathplots = pathlib.Path("plots")
s = [v["app_placed"]/v["app_total"] for v in json.loads(open(str(path.absolute()) + "/placementResults.json").read())]

fig, ax = plt.subplots()
ax.plot(t, s, 'ro-')

ax.set(xlabel='Privacy', ylabel='App Placed / Total Apps',
       title='Success in App placement with growing privacy assignment')
ax.grid()

plt.savefig(str(pathplots.absolute()) + '/privacy_placement_success.pdf',format='pdf')
plt.savefig(str(pathplots.absolute()) + '/privacy_placement_success.png',format='png')
plt.show()