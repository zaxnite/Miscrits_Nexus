import pandas as pd
import os

def sort_databases_by_id():
    """
    Sorts both miscrit_database.csv and moves_database.csv by Miscrit_ID
    """
    
    # Path to the data directory
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))
    miscrit_path = os.path.join(data_dir, "miscrit_database.csv")
    moves_path = os.path.join(data_dir, "moves_database.csv")
    
    print("Sorting databases by Miscrit_ID...")
    print("-" * 50)
    
    # Sort miscrit_database.csv
    if os.path.exists(miscrit_path):
        print(f"Loading {miscrit_path}")
        miscrit_df = pd.read_csv(miscrit_path)
        original_count = len(miscrit_df)
        
        # Sort by Miscrit_ID
        miscrit_df_sorted = miscrit_df.sort_values('Miscrit_ID').reset_index(drop=True)
        
        # Save back to CSV
        miscrit_df_sorted.to_csv(miscrit_path, index=False)
        print(f"✓ Sorted {original_count} miscrits by Miscrit_ID")
    else:
        print(f"✗ {miscrit_path} not found!")
    
    # Sort moves_database.csv
    if os.path.exists(moves_path):
        print(f"Loading {moves_path}")
        moves_df = pd.read_csv(moves_path)
        original_count = len(moves_df)
        
        # Sort by Miscrit_ID, then by Move_ID to maintain order within each miscrit
        moves_df_sorted = moves_df.sort_values(['Miscrit_ID', 'Move_ID']).reset_index(drop=True)
        
        # Save back to CSV
        moves_df_sorted.to_csv(moves_path, index=False)
        print(f"✓ Sorted {original_count} moves by Miscrit_ID (then Move_ID)")
    else:
        print(f"✗ {moves_path} not found!")
    
    print("-" * 50)
    print("Database sorting complete!")

if __name__ == "__main__":
    sort_databases_by_id()