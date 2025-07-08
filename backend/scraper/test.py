import pandas as pd

moves_path = r'D:\miscrits_nexus\data\moves_database.csv'

moves_df = pd.read_csv(moves_path)

def check_miscrit_move_count(moves_df: pd.DataFrame, expected_count: int = 12):
    """
    Checks that each Miscrit_ID in the moves DataFrame has exactly `expected_count` moves.
    Prints positive and negative responses accordingly.

    Args:
        moves_df (pd.DataFrame): The DataFrame containing move records.
        expected_count (int): Number of expected moves per Miscrit.
    """
    move_counts = moves_df["Miscrit_ID"].value_counts()

    valid_ids = move_counts[move_counts == expected_count].index.tolist()
    invalid_ids = list(move_counts[move_counts != expected_count].items())

    if valid_ids:
        print(f"✅ {len(valid_ids)} Miscrit_ID(s) have exactly {expected_count} moves.")
    
    if invalid_ids:
        print("❌ The following Miscrit_IDs do not have 12 moves:")
        for miscrit_id, count in invalid_ids:
            print(f"   - Miscrit_ID {miscrit_id}: {count} moves")
    else:
        print("🎉 All Miscrit_IDs are correctly assigned 12 moves.")

check_miscrit_move_count(moves_df,12)