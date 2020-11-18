from util.meetyourprofoptimization import solve_meet_prof_optimization
import util.constants
import numpy as np
import json
import heapq
from classes.professordate import Professor

inputdata = "data/studenten1.json"
inputprofs = "data/professoren.json"
RAND_SORT = True

#### DATE DATA
# parse json input to numpy format
with open(inputdata) as input:
    exportdata = json.load(input)

# define the data
prefs = []
studids = []
fachsems = []

# get data
for key in exportdata:
    stud = exportdata[key]

    pref = stud['prefs']
    id = stud['id']
    fachsem = stud['fachsem']

    # modify weights for 1st and 3rd semester
    if fachsem == "1":
        for i in range(len(pref)):
            pref[i] += 2

    prefs.append(pref)
    fachsems.append(fachsem)
    studids.append(id)


#### PROF DATA
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
    prof = profdata[key]

    profids.append(int(prof['prid']))
    profnames.append(prof['name'])
    profdatecnts.append(prof['anztermine'])
    profdates.append(prof['termine'])

    # just a check
    assert idx == int(prof['prid'])
    idx += 1


prof_capacities = [6*dates for dates in profdatecnts]
preferences = np.array(prefs)

assert len(prof_capacities) == len(preferences[0])

# solve the association problem
association = solve_meet_prof_optimization(bubble_capacities=prof_capacities, preferences=preferences)
association = np.array(association)

# contains all students, so that first every student gets one date, then a second
stud_heap = []

# how many students are associated to each prof
prof_stud_cnts = [0 for i in range(len(profids))]

# List for prof classes, to handle the group size and assignment
Professors = []

for prof_idx in range(len(profids)):
    assert prof_idx + 1 == profids[prof_idx]
    profstuds = np.nonzero(association[:, prof_idx])[0]
    Prof = Professor(stud_cnt=len(profstuds), student_lst=profstuds)
    Professors.append(Prof)


if RAND_SORT:

    #### RANDOM SORTING
    for Prof in Professors:
        Prof.distributeRandom()

else:
    #### INTELLIGENT SORTING
    # get data from association matrix
    stud_idx = 0
    for studentasn in association:
        studprofs = np.nonzero(studentasn)
        studid = studids[stud_idx]
        dates = tuple()
        stud_idx += 1
        print("ASN / profs / id", studentasn, studprofs[0], studid)

        heapq.heappush(stud_heap, (0, studid, tuple(studprofs), dates))


    while stud_heap:
        pass


#### READ OUT DATES FROM PROF CLASSES

membership = np.zeros((len(studids), len(profids)), dtype=np.int32)

prof_idx = 0
for Prof in Professors:
    date_idx = 1
    for date in Prof.dates:
        for stud_idx in date:
            membership[stud_idx][prof_idx] = date_idx
        date_idx += 1
    prof_idx += 1


result = dict()

for i in range(len(membership)):
    print(membership[i], preferences[i])
    studdict = dict(id=studids[i], fachsem=fachsems[i], prefs=preferences[i].tolist(), dates=membership[i].tolist())
    result[str(i)] = studdict

print(result)

with open('data/result.json', 'w') as file:
    json.dump(result, file)
    file.close()




