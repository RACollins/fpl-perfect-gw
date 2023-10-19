import pulp
import numpy as np

# random fake data for costs and values
n_total = 100
n_selected = 10
total_cost = 100
costs = np.random.uniform(low=5, high=20, size=n_total)
values = costs * np.random.uniform(low=0.9, high=1.1, size=n_total)

model = pulp.LpProblem("Constrained value maximisation", pulp.LpMaximize)
decisions = [
    pulp.LpVariable("x{}".format(i), lowBound=0, upBound=1, cat="Integer")
    for i in range(n_total)
]

# PuLP has a slightly weird syntax, but it's great. This is how to add the objective function:
model += sum(decisions[i] * values[i] for i in range(n_total)), "Objective"

# and here are the constraints
model += sum(decisions[i] * costs[i] for i in range(n_total)) <= total_cost # total cost
model += sum(decisions) <= n_selected  # total items

model.solve()

# print results
cost_of_selected_items, value_of_selected_items = [], []
for i in range(n_total):
    if decisions[i].value() == 1:
        cost_of_selected_items.append(costs[i])
        value_of_selected_items.append(values[i])
        print(i, costs[i], values[i])

print("cost_of_selected_items: {}".format(sum(cost_of_selected_items)))
print("value_of_selected_items: {}".format(sum(value_of_selected_items)))
