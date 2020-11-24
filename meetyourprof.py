from util.meetyourprofoptimization import solve_meet_prof_optimization
import util.constants
import numpy as np
import json
import heapq
from classes.professordate import Professor
from datetime import date

inputdata = "data/studenten5.json"
inputprofs = "data/professoren.json"
RAND_SORT = False
ONLY_FIRST_WEEK = False
OPTIMISE_DATES = True
EXCLUDE_WEEKS = [1]


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
profweeks = []

# get data
idx=1
for key in profdata:
    prof = profdata[key]

    profdate = prof['termine']
    datecnt = prof['anztermine']
    weeks = []

    # get the calendar week for each date
    for datestring in profdate:
        isodate = date.fromisoformat(datestring.split(' ')[0])
        weeks.append(isodate.isocalendar()[1] - 47)

    # check if weeks are excluded and refine data
    for week in weeks:
        if week in EXCLUDE_WEEKS:
            i = weeks.index(week)
            del profdate[i]
            datecnt -= 1
            del weeks[i]
            print("(STATUS) : Prepare data ", prof['name'], "deleted date in week", i+1)

    # check format
    assert datecnt == len(profdate) == len(weeks)

    profids.append(int(prof['prid']))
    profnames.append(prof['name'])

    profdatecnts.append(datecnt)
    profdates.append(profdate)
    profweeks.append(weeks)

    # just a check
    assert idx == int(prof['prid'])
    idx += 1


if ONLY_FIRST_WEEK:
    prof_capacities = [6 for dates in profdatecnts]
else:
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
    prof_stud_cnts[prof_idx] = len(profstuds)
    Prof = Professor(stud_cnt=len(profstuds), student_lst=profstuds, name=profnames[prof_idx], optim_dates=False)
    Professors.append(Prof)


print("(INFO)  : Prof student counts", prof_stud_cnts)


if RAND_SORT:

    #### RANDOM SORTING
    for Prof in Professors:
        Prof.distributeRandom()

else:
    #### INTELLIGENT SORTING
    # get data from association matrix
    stud_idx = 0
    for studentasn in association:
        studprofs = np.nonzero(studentasn)[0]
        studid = studids[stud_idx]
        # print("ASN / profs / id", studentasn, studprofs[0], studid)

        heapq.heappush(stud_heap, (0, stud_idx, studid, tuple(studprofs), [-1, -1]))
        stud_idx += 1


    while stud_heap:
        visited, stud_idx, studid, studprofs, dates = heapq.heappop(stud_heap)

        if visited > 2:
            # added all possible students
            break

        success = False

        for i in range(len(studprofs)):
            if dates[i] == -1:
                Prof = Professors[studprofs[i]]
                if not Prof.full():
                    date = Prof.getDateForStudent(stud_idx)
                    dates[i] = date
                    heapq.heappush(stud_heap, (visited+1, stud_idx, studid, studprofs, dates))
                    success = True
                    break

        if not success:
            heapq.heappush(stud_heap, (visited + 1, stud_idx, studid, studprofs, dates))



#### IMPROVE DATES BY FILLING THEM UP


if OPTIMISE_DATES:
    incomplete_dates = []

    for prof_idx in range(len(Professors)):
        Prof = Professors[prof_idx]
        if not Prof.full():
            pending_date = Prof.dates[len(Prof.dates)-1]
            spots = 6 - len(pending_date)
            profdate = spots, prof_idx, Prof.name, pending_date
            incomplete_dates.append(profdate)

    incomplete_dates = sorted(incomplete_dates, key=lambda date_tuple: date_tuple[0])

    print("(STATUS) : These dates must be optimised: ")
    for pd in incomplete_dates:
        print(pd)


    while len(incomplete_dates) > 1:
        first = incomplete_dates[0]
        last = incomplete_dates[-1]

        # print("First ", first)
        # print ("Last ", last)

        Prof_add = Professors[first[1]]
        Prof_red = Professors[last[1]]

        Prof_add.getDateForStudent(Prof_red.popStudent())

        if Prof_red.full(prints=False):
            del incomplete_dates[-1]

        if Prof_add.full(prints=False):
            del incomplete_dates[0]

        # print(incomplete_dates)


#### READ OUT DATES FROM PROF CLASSES

membership = np.zeros((len(studids), len(profids)), dtype=np.int32)

prof_idx = 0
for Prof in Professors:
    date_idx = 0
    for date in Prof.dates:
        for stud_idx in date:
            membership[stud_idx][prof_idx] = profweeks[prof_idx][date_idx]
        date_idx += 1
    prof_idx += 1


result = dict()

for i in range(len(membership)):
    # print(membership[i], preferences[i])
    studdict = dict(id=studids[i], fachsem=fachsems[i], prefs=preferences[i].tolist(), dates=membership[i].tolist())
    result[str(i)] = studdict

with open('data/result.json', 'w') as file:
    json.dump(result, file)
    file.close()


#### SOME STATS:

    cnt_stud_w_two_dates = 0
    cnt_stud_w_one_dates = 0
    cnt_stud_w_no_dates = 0
    cnt_full_dates = 0
    cnt_nfull_dates = 0
    cnt_empty_dates = 0
    cnt_overflow_studs = 0

    cnt_stud_w_two_full_dates = 0
    cnt_stud_w_one_full_dates = 0
    cnt_stud_w_no_full_dates = 0

    studs_with_no_date = []
    studs_with_one_date = []
    studs_with_two_date = []

    for stud_idx in range(len(membership)):
        studdates = np.nonzero(membership[stud_idx])[0]
        if len(studdates) is 2:
            cnt_stud_w_two_dates += 1
        elif len(studdates) is 1:
            cnt_stud_w_one_dates += 1
        else:
            cnt_stud_w_no_dates += 1

        full_date = 0
        for prof in studdates:
            for date in Professors[prof].dates:
                if stud_idx in date and len(date) == 6:
                    full_date += 1

        if full_date == 0:
            cnt_stud_w_no_full_dates += 1
            studs_with_no_date.append(stud_idx)
        elif full_date == 1:
            cnt_stud_w_one_full_dates += 1
            studs_with_one_date.append(stud_idx)
        else:
            cnt_stud_w_two_full_dates += 1
            studs_with_two_date.append(stud_idx)


    for prof_idx in range(len(membership[0])):
        Professors[prof_idx].printMyDates()
        profdates = np.nonzero(membership[:, prof_idx])[0]
        if len(profdates) is 6:
            cnt_full_dates += 1
        elif len(profdates) is 0:
            cnt_empty_dates += 1
        elif len(profdates) < 6:
            cnt_nfull_dates += 1
            cnt_overflow_studs += len(profdates)
        else:
            pass


    print("two date students: ", cnt_stud_w_two_dates)
    print("one date students: ", cnt_stud_w_one_dates)
    print("no date students: ", cnt_stud_w_no_dates)

    print("two full date students: ", cnt_stud_w_two_full_dates)
    print("one full date students: ", cnt_stud_w_one_full_dates)
    print("no full date students: ", cnt_stud_w_no_full_dates)
    print("studs with no full date:", studs_with_no_date)
    print("studs with one full date:", studs_with_one_date)
    print("studs with two full date:", studs_with_two_date)

    print("\n---Only valid for first week mode---")
    print("full dates: ", cnt_full_dates)
    print("not full dates: ", cnt_nfull_dates)
    print("empty dates: ", cnt_empty_dates)
    print("overflow studs: ", cnt_overflow_studs)










