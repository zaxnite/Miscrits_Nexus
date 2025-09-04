
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

top_miscrits = find_best_miscrits(miscrit_df, speed_preference="low", top_n=5)
print(tabulate(top_miscrits, headers='keys', tablefmt='fancy_grid'))



def speed_ratio(df: pd.DataFrame):
    """
    Counts Miscrits by speed groups and calculates the ratio.

    Args:
        df (pd.DataFrame): The Miscrit database.

    Returns:
        dict: Dictionary with counts and ratio
    """

    # rs = number of Miscrits with Speed 3, 4, 5
    red_s = df[df["Speed"].isin([4, 5])].shape[0]
    gray_s = df[df["Speed"].isin([3])].shape[0]
    # gs = number of Miscrits with Speed 1, 2
    green_s = df[df["Speed"].isin([1, 2])].shape[0]

    

    return {
        "red": red_s,
        "gray": gray_s,
        "green": green_s
    }



def filter_miscrits(df, miscrit_type=None, status_effects=None):
    """
    Filter miscrits by type and/or one or more status effects.

    Parameters:
        df (pd.DataFrame): Miscrit database DataFrame
        miscrit_type (str, optional): Element type (e.g. "Fire", "Water")
        status_effects (list[str], optional): List of status effects (e.g. ["Poison", "Sleep"])

    Returns:
        pd.DataFrame: Filtered miscrits
    """
    filtered_df = df.copy()

    if miscrit_type:
        filtered_df = filtered_df[filtered_df['Type'].str.contains(miscrit_type, case=False, na=False)]

    if status_effects:
        # Check if any of the status effects appear in 'Status Effects'
        mask = filtered_df['Status Effects'].apply(
            lambda x: any(effect.lower() in str(x).lower() for effect in status_effects)
        )
        filtered_df = filtered_df[mask]

    return filtered_df[['Miscrit_ID', 'Name', 'Type', 'Status Effects', 'Health', 'Speed']]



# crits = filter_miscrits(miscrit_df, miscrit_type="Water", status_effects=["Heal over Time", "Heal","Life Steal"])


# print(tabulate(crits, headers='keys', tablefmt='fancy_grid'))

