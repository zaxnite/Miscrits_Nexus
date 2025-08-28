import pandas as pd
from miscrit_scraper import miscrit_info
from miscrit_move import scrape_moves_info
import os
import time

# Column definitions
columns_miscrits = ['Miscrit_ID', 'Name', 'Rarity', 'Location', 'Type', 'Evolutions',
                    'Health', 'Speed', 'Elemental Attack', 'Elemental Defense',
                    'Physical Attack', 'Physical Defense','Status Effects','Image_Name']
columns_moves = ['Miscrit_ID', 'Move_Name', 'Element', 'AP', 'Accuracy', 'Description', 'Enchant']


data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))
moves_path = os.path.join(data_dir, "moves_database.csv")
miscrit_path = os.path.join(data_dir, "miscrit_database.csv")


os.makedirs(data_dir, exist_ok=True)


if os.path.exists(miscrit_path):
    miscrit_df = pd.read_csv(miscrit_path)
    existing_miscrit_ids = set(miscrit_df["Miscrit_ID"])
else:
    miscrit_df = pd.DataFrame(columns=columns_miscrits)
    existing_miscrit_ids = set()

if os.path.exists(moves_path):
    moves_df = pd.read_csv(moves_path, index_col="Move_ID")
    next_move_id = moves_df.index.max() + 1
else:
    moves_df = pd.DataFrame(columns=columns_moves)
    next_move_id = 1

def database_adder(index: int):
    global miscrit_df, moves_df, next_move_id, existing_miscrit_ids

    if index in existing_miscrit_ids:
        print(f" Miscrit ID {index} already exists. Skipping.")
        return

    try:
       
        miscrit = miscrit_info(index)
        moves = miscrit.get('Abilities')
        miscrit_moves = scrape_moves_info(index, moves)
        miscrit.pop('Abilities')

        miscrit_df.loc[len(miscrit_df)] = miscrit
        existing_miscrit_ids.add(index)
        
        for move in miscrit_moves:
            moves_df.loc[next_move_id] = move
            next_move_id += 1

    except Exception as e:
        print(f" Error at Miscrit ID {index}: {e}")

if __name__ == "__main__":
    working_index = [591, 592, 593, 594, 595, 596, 597, 598, 599, 600, 601, 602]
    start = time.perf_counter()
    for i in working_index:  
        print(f" Scraping Miscrit ID: {i}")
        database_adder(i)

    
    miscrit_df.set_index("Miscrit_ID", inplace=True)
    moves_df.index.name = "Move_ID"

    print(" Done scraping!")
    print(f"Total Miscrits: {len(miscrit_df)}")
    print(f"Total Moves: {len(moves_df)}")

    
    miscrit_df.to_csv(miscrit_path, index=True)
    moves_df.to_csv(moves_path, index=True)

    end = time.perf_counter()

    print(f"Took {end - start:.4f} seconds")

