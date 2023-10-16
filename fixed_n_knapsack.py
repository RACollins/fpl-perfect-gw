import numpy as np

def knapsack(n, k, w):
    if (n, k, w) not in knapsack.t:
        if w < 0 or n < 0 or k < 0:
            knapsack.t[(n, k, w)] = -1000  # big negative number, large enough that solution is invalid
        elif n < k:
            knapsack.t[(n, k, w)] = -1000 # presuming you want exactly k items; remove this line if <= k is okay
        elif k == 0:
            knapsack.t[(n, k, w)] = 0
        else:
            knapsack.t[(n, k, w)] = max(knapsack(n-1, k, w), data[n-1, 0] + knapsack(n-1, k-1, w-data[n-1,1]))
    return knapsack.t[(n, k, w)]
knapsack.t = {}

def traceback_solution(t, n, k, w):
    if k <= 0:
        return
    s = t[(n, k, w)]
    a = t[(n-1, k, w)]
    b = data[n-1, 0] + t[(n-1, k-1, w-data[n-1, 1])]
    if s == a:
        yield from traceback_solution(t, n-1, k, w)
    elif s == b:
        yield (n-1, data[n-1])
        yield from traceback_solution(t, n-1, k-1, w-data[n-1, 1])
    else:
        raise Exception("Error message")

if __name__ == "__main__":

    n_items_total, k_items_solution, max_weight = 100, 5, 100
    data = np.random.randint(0, max_weight+1, (n_items_total,2))
    best_score = knapsack(n_items_total, k_items_solution, max_weight)
    print(type(knapsack.t))
    solution = list(traceback_solution(knapsack.t, n_items_total, k_items_solution, max_weight))

    print(solution)