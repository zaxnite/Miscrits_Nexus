import pandas as pd
import numbers

miscrit_path = r'D:\miscrits_nexus\data\miscrit_database.csv'
moves_path = r'D:\miscrits_nexus\data\moves_database.csv'

miscrit_df = pd.read_csv(miscrit_path)
moves_df = pd.read_csv(moves_path)

def database_checker(df: pd.DataFrame, expected_types: dict = None):
    errors = []

    # Null or Empty Checker
    is_null_or_empty = df.isnull() | (df.astype(str).map(str.strip) == "")
    null_or_empty_rows = df[is_null_or_empty.any(axis=1)].index
    if not null_or_empty_rows.empty:
        errors.append(("Null or Empty Values", null_or_empty_rows.tolist()))

    # Duplicate Checker
    duplicate_rows = df[df.duplicated()].index
    if not duplicate_rows.empty:
        errors.append(("Duplicate Rows", duplicate_rows.tolist()))

    # Data Type Checker
    if expected_types:
        wrong_type_rows = pd.Series([False] * len(df), index=df.index)
        for col, expected_type in expected_types.items():
            if col in df.columns:
                if expected_type == int:
                    wrong_type_mask = ~df[col].apply(lambda x: pd.api.types.is_integer(x) or (isinstance(x, numbers.Number) and float(x).is_integer()))
                elif expected_type == float:
                    wrong_type_mask = ~df[col].apply(lambda x: isinstance(x, numbers.Number))
                else:
                    wrong_type_mask = ~df[col].apply(lambda x: isinstance(x, expected_type))
                wrong_type_rows |= wrong_type_mask
        if wrong_type_rows.any():
            errors.append(("Wrong Data Types", df[wrong_type_rows].index.tolist()))

    return errors

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

expected_types_miscrit = {
    "Miscrit_ID": int,
    "Name": str,
    "Rarity": str,
    "Location": str,
    "Type": str,
    "Evolutions": str,
    "Health": int,
    "Speed": int,
    "Elemental Attack": int,
    "Elemental Defense": int,
    "Physical Attack": int,
    "Physical Defense": int
}

expected_types_moves = {
    "Move_ID": int,
    "Miscrit_ID": int,
    "Move_Name": str,
    "Element": str,
    "AP": str,  
    "Accuracy": str,
    "Description": str,
    "Enchant": str
}

check_miscrit_move_count(moves_df,12)

issues = database_checker(moves_df, expected_types_moves)

if not issues:
    print("✅ No issues found in the Miscrit database.")
else:
    for issue_type, rows in issues:
        print(f"❌ {issue_type} found in rows: {rows}")
