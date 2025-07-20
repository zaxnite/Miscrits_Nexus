
import pandas as pd
from tabulate import tabulate

miscrit_path = r'D:\miscrits_nexus\data\miscrit_database.csv'
moves_path = r'D:\miscrits_nexus\data\moves_database.csv'

miscrit_df = pd.read_csv(miscrit_path)
moves_df = pd.read_csv(moves_path)


def find_best_miscrits(df: pd.DataFrame, speed_preference: str = "any", top_n: int = 5):
    """
    Finds Miscrits with the best average defense, best offensive stat (EA/PA),
    and filters based on speed preference.

    Args:
        df (pd.DataFrame): The Miscrit database.
        speed_preference (str): "low", "high", or "any"
        top_n (int): Number of top Miscrits to return

    Returns:
        pd.DataFrame: Filtered and sorted Miscrits
    """

    # Calculate defense average
    df["defense_avg"] = df[["Health", "Elemental Defense", "Physical Defense"]].mean(axis=1)

    # Calculate best offense between Elemental Attack or Physical Attack
    df["best_offense"] = df[["Elemental Attack", "Physical Attack"]].max(axis=1)

    # Filter by speed preference
    if speed_preference == "low":
        df = df[df["Speed"] <= 2]  # assuming 1-5 scale
    elif speed_preference == "high":
        df = df[df["Speed"] >= 4]

    # Final score (you can weight these if needed)
    #df["score"] = df["defense_avg"] + df["best_offense"]
    df.loc[:, "score"] = df["defense_avg"] + df["best_offense"]


    # Sort by score
    result = df.sort_values(by="score", ascending=False).head(top_n)

    return result[[
        "Name", "Health", "Elemental Defense", "Physical Defense",
        "Elemental Attack", "Physical Attack", "Speed", "score"
    ]]

top_miscrits = find_best_miscrits(miscrit_df, speed_preference="high", top_n=5)
print(tabulate(top_miscrits, headers='keys', tablefmt='fancy_grid'))