
from __future__ import print_function
from ortools.graph import pywrapgraph
from util import util
import numpy as np


def main():
    num_students = 5
    num_bubbles = 2
    max_bubble_size = 3

    preference_costs = [20, 15, 6, 3, 1]

    # input from web formula
    preferences = np.array([[4,5], [1,5], [3,4], [1,1], [2,4]])

    start_nodes = []
    end_nodes = []
    capacities = []
    unit_costs = []

    stud_count = len(preferences)

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
            end_nodes.append(stud_count + 1 + bubble_idx)
            capacities.append(1)
            unit_costs.append(preferences[stud_idx][bubble_idx])

    for bubble_idx in range(num_bubbles):
        # make edges from bubbles to sink
        start_nodes.append(stud_count + 1 + bubble_idx)
        end_nodes.append(stud_count + num_bubbles + 1)
        capacities.append(max_bubble_size)
        unit_costs.append(0)

    supplies = [0 for i in range(stud_count + num_bubbles + 2)]
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
    else:
        print('There was an issue with the min cost flow input.')


if __name__ == "__main__":
    main()