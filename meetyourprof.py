from util.meetyourprofoptimization import solve_meet_prof_optimization
import util.constants
import numpy as np
import json

# parse json input to numpy format
inputdata = "data/exportdata.json"

with open(inputdata) as input:
    exportdata = json.load(input)

# define the data
prefs = []
ids = []
fachsems = []

# get data
for key in exportdata:
    print(key)
    stud = exportdata[key]

    pref = stud['prefs']
    id = stud['ids']
    fachsem = stud['fachsem']

    # modify weights for 1st and 3rd semester
    if fachsem == 1:
        pref += 2

    prefs.append(pref)
    fachsems.append(fachsem)
    ids.append(id)

prof_capacities = [24 for i in range()]


# test numpy data
preferences = np.array([[0, 1, 0],
                        [0, 3, 0],
                        [2, 3, 0],
                        [1, 1, 0],
                        [0, 0, 1]])

prof_capacities = [24, 24, 24]

# solve the association problem
association = solve_meet_prof_optimization(bubble_capacities=prof_capacities, preferences=preferences)



