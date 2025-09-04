import pandas as pd
import numbers

miscrit_path = r'D:\miscrits_nexus\data\miscrit_database.csv'
moves_path = r'D:\miscrits_nexus\data\moves_database.csv'

def database_checker(df: pd.DataFrame, expected_types: dict = None):
    issues = []

    # Null or Empty Checker
    is_null_or_empty = df.isnull() | (df.astype(str).map(str.strip) == "")
    for column in df.columns:
        # Skip Status Effects column for null checks since None is valid
        if column == 'Status Effects':
            continue
        null_rows = df[is_null_or_empty[column]]
        if not null_rows.empty:
            issues.append((f"Empty/Null values in '{column}'", null_rows['Miscrit_ID'].tolist()))

    # Duplicate Checker
    duplicate_rows = df[df.duplicated()]
    if not duplicate_rows.empty:
        issues.append(("Duplicate Entries", duplicate_rows['Miscrit_ID'].tolist()))

    # Data Type Checker
    if expected_types:
        for col, expected_type in expected_types.items():
            if col in df.columns:
                if col == 'Status Effects':
                    # Special handling for Status Effects to allow None values
                    wrong_type_mask = ~df[col].apply(lambda x: isinstance(x, str) or pd.isna(x))
                elif expected_type == int:
                    wrong_type_mask = ~df[col].apply(lambda x: pd.api.types.is_integer(x) or (isinstance(x, numbers.Number) and float(x).is_integer()))
                elif expected_type == float:
                    wrong_type_mask = ~df[col].apply(lambda x: isinstance(x, numbers.Number))
                else:
                    wrong_type_mask = ~df[col].apply(lambda x: isinstance(x, expected_type))
                
                wrong_type_rows = df[wrong_type_mask]
                if not wrong_type_rows.empty:
                    issues.append((f"Wrong type in '{col}' (expected {expected_type.__name__})", wrong_type_rows['Miscrit_ID'].tolist()))

    return issues

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
    "Physical Defense": int,
    "Status Effects": str,  # Changed from str or None to just str since we handle None separately
    "Image_Name": str
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

def check_status_effect_abbreviations(df: pd.DataFrame) -> list:
    """
    Checks for abbreviated status effects in the Status Effects column
    Returns a list of rows with abbreviated forms
    """
    abbreviations = {
        "Hot": "Heal over Time",
        "Dot": "Damage over Time",
        "SI": "Sleep Immunity",
        "CI": "Confuse Immunity",
        "PI": "Paralyze Immunity",
        "AI": "Antiheal Immunity",
        "A I": "Antiheal Immunity"
    }
    
    issues = []
    valid_status_rows = df[~df['Status Effects'].isna() & (df['Status Effects'] != '')]
    
    for _, row in valid_status_rows.iterrows():
        effects = [effect.strip() for effect in str(row['Status Effects']).split(',')]
        for effect in effects:
            if effect and effect in abbreviations:
                issues.append({
                    'miscrit_id': row['Miscrit_ID'],
                    'name': row['Name'],
                    'found': effect,
                    'should_be': abbreviations[effect]
                })
    
    return issues

def main():
    # Load DataFrames
    miscrit_df = pd.read_csv(miscrit_path)
    moves_df = pd.read_csv(moves_path)

    print("\n=== Checking Miscrit Move Count ===")
    check_miscrit_move_count(moves_df, 12)

    print("\n=== Checking Moves Database ===")
    moves_issues = database_checker(moves_df, expected_types_moves)
    if not moves_issues:
        print("✅ No issues found in the Moves database.")
    else:
        for issue_type, rows in moves_issues:
            print(f"❌ {issue_type} found in ids: {rows}")

    print("\n=== Checking Miscrit Database ===")
    miscrit_issues = database_checker(miscrit_df, expected_types_miscrit)
    if not miscrit_issues:
        print("✅ No issues found in the Miscrit database.")
    else:
        for issue_type, rows in miscrit_issues:
            print(f"❌ {issue_type} found in ids: {rows}")

    print("\n=== Checking for Status Effect Abbreviations ===")
    abbreviated_effects = check_status_effect_abbreviations(miscrit_df)
    if abbreviated_effects:
        print("❌ Found abbreviated status effects:")
        for issue in abbreviated_effects:
            print(f"   Miscrit ID {issue['miscrit_id']}: {issue['name']} - '{issue['found']}' should be '{issue['should_be']}'")
    else:
        print("✅ No abbreviated status effects found.")

if __name__ == "__main__":
    main()
