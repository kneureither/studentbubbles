from studentbubbles import solve_bubble_optimization
import numpy as np
import time

if __name__ == "__main__":
    # define the data
    number_of_students = 400
    number_of_bubbles = 12

    preferences = np.random.randint(low=1, high=5, size=(400, 12))
    bubble_capacities = [35 for i in range(number_of_bubbles)]

    # make sure, there is one five star prio for each student
    for i in range(len(preferences)):
        pref_five_pos = np.random.randint(1, len(bubble_capacities))
        preferences[i][pref_five_pos] = 5


    # solve the membership problem
    start_time = time.time()
    membership = solve_bubble_optimization(preferences, bubble_capacities)
    print("--- %s seconds ---" % (time.time() - start_time))

    print("\n\n")
    for i in range(len(membership)):
        print("pref: ", preferences[i], " result: ", membership[i])

