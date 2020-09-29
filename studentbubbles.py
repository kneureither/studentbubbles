
from __future__ import print_function
from ortools.graph import pywrapgraph
from util import util
import numpy as np


def solve_bubble_optimization(preferences=np.array([[4,5], [1,5], [3,4], [1,1], [2,4]]), max_bubble_size=3):
    num_students = len(preferences)
    num_bubbles = len(preferences[0])

    # define costs for different preferences
    preference_costs = [10, 5, 2, -2, -5]
    # for evaluation of ordering success
    student_got_priority = [0,0,0,0,0]
    # create the membership matrix for result
    membership = [[0 for i in range(num_bubbles)] for j in range(num_students)]

    # store graph
    start_nodes = []
    end_nodes = []
    capacities = []
    unit_costs = []

    for stud_idx, stud_prefs in enumerate(preferences):
        # make edges from source to each student
        start_nodes.append(0)
        end_nodes.append(stud_idx+1)
        capacities.append(1)
        unit_costs.append(0)

    for stud_idx, stud_prefs in enumerate(preferences):
        for bubble_idx, bubble_pref in enumerate(stud_prefs):
            # make edges from students to bubbles
            start_nodes.append(stud_idx+1)
            end_nodes.append(num_students + 1 + bubble_idx)
            capacities.append(1)
            unit_costs.append(preference_costs[preferences[stud_idx][bubble_idx] - 1])

    for bubble_idx in range(num_bubbles):
        # make edges from bubbles to sink
        start_nodes.append(num_students + 1 + bubble_idx)
        end_nodes.append(num_students + num_bubbles + 1)
        capacities.append(max_bubble_size)
        unit_costs.append(0)

    supplies = [0 for i in range(num_students + num_bubbles + 2)]
    supplies[0] = num_students
    supplies[len(supplies) - 1] = -num_students

    print("start_nodes", start_nodes)
    print("end_nodes  ", end_nodes)
    print("capacities ", capacities)
    print("unit_costs ", unit_costs)
    print("supplies   ", supplies)

    # Instantiate a SimpleMinCostFlow solver.
    min_cost_flow = pywrapgraph.SimpleMinCostFlow()

    # Add each arc.
    for i in range(0, len(start_nodes)):
        start_node = int(start_nodes[i])
        end_node = int(end_nodes[i])
        capacity = int(capacities[i])
        unit_cost = int(unit_costs[i])
        min_cost_flow.AddArcWithCapacityAndUnitCost(start_node, end_node, capacity, unit_cost)

    # Add node supplies.
    for i in range(0, len(supplies)):
        min_cost_flow.SetNodeSupply(i, supplies[i])

    # Find the minimum cost flow between node 0 and node 4.
    if min_cost_flow.Solve() == min_cost_flow.OPTIMAL:
        print('Minimum cost:', min_cost_flow.OptimalCost())
        print('')
        print('  Arc    Flow / Capacity  Cost')
        for i in range(min_cost_flow.NumArcs()):
            cost = min_cost_flow.Flow(i) * min_cost_flow.UnitCost(i)
            print('%1s -> %1s   %3s  / %3s       %3s' % (
                min_cost_flow.Tail(i),
                min_cost_flow.Head(i),
                min_cost_flow.Flow(i),
                min_cost_flow.Capacity(i),
                cost))

        print("")

        # get the relevant edges
        for student_idx in range(num_students):
            for stud_bubble_idx in range(num_bubbles):
                i = num_students + student_idx * num_bubbles + stud_bubble_idx

                cost = min_cost_flow.Flow(i) * min_cost_flow.UnitCost(i)
                print('%1s -> %1s   %3s  / %3s       %3s' % (
                    min_cost_flow.Tail(i),
                    min_cost_flow.Head(i),
                    min_cost_flow.Flow(i),
                    min_cost_flow.Capacity(i),
                    cost))

                student = min_cost_flow.Tail(i) - 1
                bubble = min_cost_flow.Head(i) - num_students - 1
                flow = min_cost_flow.Flow(i)

                membership[student][bubble] = flow
                if cost != 0:
                    pref = preference_costs.index(cost)
                    student_got_priority[pref] += 1

        print("\n\nResult:")
        for pref, pref_count in enumerate(student_got_priority):
            print('priority : %s student count : %s  (%2.1f percent)' % (pref + 1, pref_count, pref_count/ float(num_students) * 100))

    else:
        print('There was an issue with the min cost flow input.')



    return membership




if __name__ == "__main__":
    # define the data
    preferences = np.array([[4,5], [1,5], [3,4], [1,1], [2,4], [1,1]])
    max_bubble_size = 3

    # solve the membership problem
    membership = solve_bubble_optimization(preferences, max_bubble_size)

    print("\n\n")
    print(membership)