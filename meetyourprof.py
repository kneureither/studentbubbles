from util.meetyourprofoptimization import solve_meet_prof_optimization
import util.constants
import numpy as np
import json
import heapq

#### DATE DATA
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
    id = stud['id']
    fachsem = stud['fachsem']

    # modify weights for 1st and 3rd semester
    if fachsem == 1:
        pref += 2

    prefs.append(pref)
    fachsems.append(fachsem)
    ids.append(id)


#### PROF DATA


inputprofs = "data/professoren.json"

with open(inputprofs) as input:
    profdata = json.load(input)

# define the data
profids=[]
profnames = []
profdatecnts = []
profdates = []

# get data
idx=1
for key in profdata:
    print(key)
    prof = profdata[key]

    profids.append(int(prof['prid']))
    profnames.append(prof['name'])
    profdatecnts.append(prof['anztermine'])
    profdates.append(prof['termine'])

    # just a check
    assert idx == int(prof['prid'])
    idx += 1



# make this somehow nice
prof_capacities = [24 for i in range(3)]


# test numpy data
preferences = np.array([[0, 1, 0],
                        [0, 3, 0],
                        [2, 3, 0],
                        [1, 1, 0],
                        [0, 0, 1]])

prof_capacities = [24, 24, 24]

# solve the association problem
association = solve_meet_prof_optimization(bubble_capacities=prof_capacities, preferences=preferences)


stud_heap = []

# heapq data format (no. groups, id, (prof 1, prof 2), (date 1, date 2))
# pop one student, associate date, update tuple, push back to queue.
# prof list with stud count and date return.

# stud_heap.append((0, 0, (0,0)))


