from studentbubbles import solve_bubble_optimization
from studentbubbles import calculate_result_quality
import numpy as np
import matplotlib.pyplot as plt
import time

if __name__ == "__main__":
    # define the data
    number_of_students = 452
    number_of_bubbles = 12

    mode = "binomial"

    if mode=="binomial":
        preferences = np.random.binomial(5, 0.1, size=(number_of_students, number_of_bubbles))
    else:
        preferences = np.random.randint(1, high=5, size=(number_of_students, number_of_bubbles))
    preferences[preferences < 1] = 1
    bubble_capacities = [35 for i in range(number_of_bubbles)]

    # make sure, there is one five star prio for each student
    for i in range(len(preferences)):
        pref_five_pos = np.random.randint(1, len(bubble_capacities)/2)
        preferences[i][pref_five_pos] = 5


    preference_cost_vecs = [[6, 5, 2, -2, -5],
                            [6, 5, 1, -3, -5],
                            [10, 5, 2, -2, -5],
                            [40, 5, 2, -2, -5],
                            [40, 10, 1, -3, -5]]

    preference_stars = np.array([1, 2, 3, 4, 5])

    student_allocation_result=[]

    for preference_costs in preference_cost_vecs:
        print("Testing pref costs: ", preference_costs)

        # solve the membership problem
        start_time = time.time()
        membership = solve_bubble_optimization(preferences, bubble_capacities, preference_costs)
        result = calculate_result_quality(preferences, membership)
        print("result: ", result)
        student_allocation_result.append(result)
        print("--- %s seconds ---" % (time.time() - start_time))

        print("\n\n")

        assert (len(membership) == number_of_students)
        assert (len(membership[0]) == number_of_bubbles);

        for i in range(len(membership)):
            # check if there is only one bubble assigned for each student
            assert (membership[i].count(1) == 1)
            # print("pref: ", preferences[i], " result: ", membership[i])

    plt.title("Results for different cost vectors (" + mode + " data)")

    number_of_bars = len(preference_cost_vecs)
    for i in range(number_of_bars):
        offset = i * 0.7/float(number_of_bars-1) - 0.35
        print("offset: ", offset)
        X = preference_stars + offset
        Y = np.array(student_allocation_result[i])
        plt.bar(X,Y, width=0.8/float(number_of_bars), label="costs: " + str(preference_cost_vecs[i]))

    plt.xlabel("priorities of assigned groups")
    plt.ylabel("number of students")

    plt.legend()
    plt.savefig("plots/priority_distribution_stud" + str(number_of_students) + "_bub" + str(number_of_bubbles) + "_" + mode + ".pdf")









