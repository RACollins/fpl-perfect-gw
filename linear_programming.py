import pulp
import numpy as np

# random fake data for costs and values
costs = np.random.uniform(low=5, high=20, size=100)
values = costs * np.random.uniform(low=0.9, high=1.1, size=100)

model = pulp.LpProblem("Constrained value maximisation", pulp.LpMaximize)
decisions = [pulp.LpVariable("x{}".format(i), lowBound=0, upBound=1, cat='Integer')
             for i in range(100)]

# PuLP has a slightly weird syntax, but it's great. This is how to add the objective function:
model += sum(decisions[i] * values[i] for i in range(100)), "Objective"

# and here are the constraints
model += sum(decisions[i] * costs[i] for i in range(100)) <= 100  # total cost
model += sum(decisions) <= 10  # total items

model.solve()

# print results
for i in range(100):
    if decisions[i].value() == 1:
        print(i, costs[i], values[i])