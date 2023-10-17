import numpy as np
from download import download_from_github


def knapsack(data, n, k, w):
    if (n, k, w) not in knapsack.t:
        if w < 0 or n < 0 or k < 0:
            knapsack.t[
                (n, k, w)
            ] = -1000  # big negative number, large enough that solution is invalid
        elif n < k:
            knapsack.t[
                (n, k, w)
            ] = (
                -1000
            )  # presuming you want exactly k items; remove this line if <= k is okay
        elif k == 0:
            knapsack.t[(n, k, w)] = 0
        else:
            knapsack.t[(n, k, w)] = max(
                knapsack(data, n - 1, k, w),
                data[n - 1, 0] + knapsack(data, n - 1, k - 1, w - data[n - 1, 1]),
            )
    return knapsack.t[(n, k, w)]


knapsack.t = {}


def traceback_solution(data, t, n, k, w):
    if k <= 0:
        return
    s = t[(n, k, w)]
    a = t[(n - 1, k, w)]
    b = data[n - 1, 0] + t[(n - 1, k - 1, w - data[n - 1, 1])]
    if s == a:
        yield from traceback_solution(data, t, n - 1, k, w)
    elif s == b:
        yield (n - 1, data[n - 1])
        yield from traceback_solution(data, t, n - 1, k - 1, w - data[n - 1, 1])
    else:
        raise Exception("Error message.")


def main():
    df = download_from_github(season="2023-24", gw=7)

    # n_items_total, k_items_solution, max_weight = 100, 5, 100
    n_items_total = df.shape[0]
    k_items_solution = 15
    max_weight = 1000

    # data = np.random.randint(0, max_weight+1, (n_items_total,2))
    data = df.loc[:, ["total_points", "value"]].values

    best_score = knapsack(data, n_items_total, k_items_solution, max_weight)
    print(type(knapsack.t))
    solution = list(
        traceback_solution(data, knapsack.t, n_items_total, k_items_solution, max_weight)
    )
    solution_index = [t[0] for t in solution]
    solution_df = df.loc[solution_index, :]

    print("Best squad")
    print(solution_df.loc[:, ["name", "team", "position", "total_points", "value"]].sort_values(["total_points"], ascending=False))
    print("")

    print("Team counts")
    print(solution_df.loc[:, "team"].value_counts())
    print("")
    
    print("Position counts")
    print(solution_df.loc[:, "position"].value_counts())
    print("")
    
    print("Squad value and total points")
    print(solution_df.loc[:, ["total_points", "value"]].sum())
    return None


if __name__ == "__main__":
    main()
