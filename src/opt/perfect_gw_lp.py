import pulp
import numpy as np
import pandas as pd
import sys
import os
import argparse


sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../..")
from src.data.download import download_from_github


def select_team(
    expected_scores, prices, positions, clubs, total_budget, sub_factor
):
    print(total_budget)
    num_players = len(expected_scores)
    model = pulp.LpProblem("Constrained value maximisation", pulp.LpMaximize)
    decisions = [
        pulp.LpVariable("x{}".format(i), lowBound=0, upBound=1, cat="Integer")
        for i in range(num_players)
    ]
    captain_decisions = [
        pulp.LpVariable("y{}".format(i), lowBound=0, upBound=1, cat="Integer")
        for i in range(num_players)
    ]
    sub_decisions = [
        pulp.LpVariable("z{}".format(i), lowBound=0, upBound=1, cat="Integer")
        for i in range(num_players)
    ]

    # objective function:
    model += (
        sum(
            (captain_decisions[i] + decisions[i] + sub_decisions[i] * sub_factor)
            * expected_scores[i]
            for i in range(num_players)
        ),
        "Objective",
    )

    # cost constraint
    model += (
        sum((decisions[i] + sub_decisions[i]) * prices[i] for i in range(num_players))
        <= total_budget
    )  # total cost

    # position constraints
    # 1 starting goalkeeper
    model += sum(decisions[i] for i in range(num_players) if positions[i] == "GK") == 1
    # 2 total goalkeepers
    model += (
        sum(
            decisions[i] + sub_decisions[i]
            for i in range(num_players)
            if positions[i] == "GK"
        )
        == 2
    )

    # 3-5 starting defenders
    model += sum(decisions[i] for i in range(num_players) if positions[i] == "DEF") >= 3
    model += sum(decisions[i] for i in range(num_players) if positions[i] == "DEF") <= 5
    # 5 total defenders
    model += (
        sum(
            decisions[i] + sub_decisions[i]
            for i in range(num_players)
            if positions[i] == "DEF"
        )
        == 5
    )

    # 3-5 starting midfielders
    model += sum(decisions[i] for i in range(num_players) if positions[i] == "MID") >= 3
    model += sum(decisions[i] for i in range(num_players) if positions[i] == "MID") <= 5
    # 5 total midfielders
    model += (
        sum(
            decisions[i] + sub_decisions[i]
            for i in range(num_players)
            if positions[i] == "MID"
        )
        == 5
    )

    # 1-3 starting attackers
    model += sum(decisions[i] for i in range(num_players) if positions[i] == "FWD") >= 1
    model += sum(decisions[i] for i in range(num_players) if positions[i] == "FWD") <= 3
    # 3 total attackers
    model += (
        sum(
            decisions[i] + sub_decisions[i]
            for i in range(num_players)
            if positions[i] == "FWD"
        )
        == 3
    )

    # club constraint
    for club_id in np.unique(clubs):
        model += (
            sum(
                decisions[i] + sub_decisions[i]
                for i in range(num_players)
                if clubs[i] == club_id
            )
            <= 3
        )  # max 3 players

    model += sum(decisions) == 11  # total team size
    model += sum(captain_decisions) == 1  # 1 captain

    for i in range(num_players):
        model += (
            decisions[i] - captain_decisions[i]
        ) >= 0  # captain must also be on team
        model += (decisions[i] + sub_decisions[i]) <= 1  # subs must not be on team

    model.solve()
    print("Total expected score = {}".format(model.objective.value()))
    decisions_bin = [int(d.value()) for d in decisions]
    captain_decisions_bin = [int(d.value()) for d in captain_decisions]
    sub_decisions_bin = [int(d.value()) for d in sub_decisions]

    return decisions_bin, captain_decisions_bin, sub_decisions_bin


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--season", type=str)
    parser.add_argument("-gw", "--goal_week", type=int)
    parser.add_argument("-tb", "--total_budget", type=float)
    parser.add_argument("-sf", "--sub_factor", type=float, default=0.0)
    args = parser.parse_args()

    df = download_from_github(season=args.season, gw=args.goal_week)
    df_reduced = df.loc[:, ["name", "position", "team", "total_points", "value"]]
    decisions_bin, captain_decisions_bin, sub_decisions_bin = select_team(
        expected_scores=df_reduced["total_points"],
        prices=df_reduced["total_points"],
        positions=df_reduced["position"],
        clubs=df_reduced["team"],
        total_budget=args.total_budget*10,
        sub_factor=args.sub_factor,
    )
    df_reduced["selected"] = decisions_bin
    df_reduced["captain"] = captain_decisions_bin
    df_reduced["substitute"] = sub_decisions_bin

    df_squad = df_reduced.loc[
        (df_reduced["selected"] == 1) | (df_reduced["substitute"] == 1), :
    ]
    df_squad["actual_points"] = np.where(
        df_squad.loc[:, "substitute"] == 1,
        0,
        np.where(
            df_squad.loc[:, "captain"] == 1,
            df_squad.loc[:, "total_points"] * 2,
            df_squad.loc[:, "total_points"],
        ),
    )
    print(df_squad)
    print(df_squad.loc[:, ["value", "actual_points"]].sum())
    return None


if __name__ == "__main__":
    main()
