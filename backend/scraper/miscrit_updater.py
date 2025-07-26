import pandas as pd
import os
from miscrit_scraper import miscrit_info
from miscrit_move import scrape_moves_info


data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))
moves_path = os.path.join(data_dir, "moves_database.csv")
miscrit_path = os.path.join(data_dir, "miscrit_database.csv")

miscrit_df = pd.read_csv(miscrit_path)
moves_df = pd.read_csv(moves_path)

#miscrits= ['Vhisp', 'Zappup', 'Dark Breezycheeks', 'Dark Lumera', 'Light Weevern', 'Light Grubbean', 'Boltzee','Beelzebug', 'Flaring', 'Gemix', 'Shurikoon', 'Light Snorkels', 'Dark Poltergust', 'Light Ignios', 'Splender', 'Dark Snortus', 'Foil Croaky', 'Sol', 'Podo', 'Inferno', 'Freedom', 'Valentino', 'Ekkult', 'Alpha', 'Nanaslug', 'Shellbee', 'Statikat', 'Aria', 'Luna', 'Hippoke', 'Leggy', 'Whik', 'Hawkai', 'Nibbles', 'Crabbles', 'Rafiery', 'Squirmle', 'Peekly', 'Dark Shellbee', 'Dark Aria', 'Light Sparkspeck', 'Light Hawkai', 'Dark Vexie', 'Waddles']
miscrits =[]


def miscrit_id_finder(miscrits: list) -> str:
    crit_ids = []
    for x in miscrits:
        matching_crit = miscrit_df.loc[miscrit_df['Name'] == x, ['Miscrit_ID']]
        crit_dict = matching_crit.to_dict(orient="records")
        if crit_dict:  # Only add if match found
            crit = crit_dict[0]
            crit_ids.append(crit['Miscrit_ID'])
    return crit_ids


def miscrit_updater(crit_ids: list):
    for i in crit_ids:
        # Get updated Miscrit data
        miscrit_data = miscrit_info(i)
        miscrit_id = miscrit_data['Miscrit_ID']
        abilities = miscrit_data['Abilities']  # Used only for scraping moves
        print(f"\n[INFO] Updating Miscrit: {miscrit_data['Name']} (ID: {miscrit_id})")

        # Remove 'Abilities' before saving to miscrit_df
        miscrit_data_clean = {k: v for k, v in miscrit_data.items() if k != 'Abilities'}

        # ---- Update miscrit_df ----
        if miscrit_id in miscrit_df['Miscrit_ID'].values:
            for col in miscrit_df.columns:
                if col in miscrit_data_clean:
                    miscrit_df.loc[miscrit_df['Miscrit_ID'] == miscrit_id, col] = miscrit_data_clean[col]
        else:
            new_row = {col: miscrit_data_clean.get(col, "") for col in miscrit_df.columns}
            miscrit_df.loc[len(miscrit_df)] = new_row

        # ---- Get and update move data ----
        new_moves = scrape_moves_info(miscrit_id, abilities)

        print(f"[INFO] Scraped {len(new_moves)} moves for Miscrit ID {miscrit_id}")
        if len(new_moves) != 12:
            print(f"[ERROR] Expected 12 moves but got {len(new_moves)}. Skipping move update.")
            continue

        # Get existing moves for the miscrit
        existing_moves = moves_df[moves_df['Miscrit_ID'] == miscrit_id].sort_values(by="Move_ID").reset_index()

        # Replace existing moves one-by-one if needed
        for idx in range(12):
            new_move = new_moves[idx]

            required_keys = ['Move_Name', 'Element', 'AP', 'Accuracy', 'Description', 'Enchant']
            if not all(k in new_move for k in required_keys):
                print(f"[ERROR] Move at index {idx} is missing keys: {new_move}")
                continue

            if idx < len(existing_moves):
                row_index = existing_moves.loc[idx, 'index']
                existing_row = moves_df.loc[row_index]
                updated = False

                for field in required_keys:
                    if existing_row[field] != new_move[field]:
                        updated = True
                        print(f" - Move changed at position {idx + 1}: '{existing_row['Move_Name']}' → '{new_move['Move_Name']}'")
                        break

                if updated:
                    for field in required_keys:
                        moves_df.loc[row_index, field] = new_move[field]
                else:
                    print(f" - Move unchanged at position {idx + 1}: '{existing_row['Move_Name']}'")

            else:
                print(f"[WARN] Less than 12 moves exist for Miscrit ID {miscrit_id}, adding missing move.")
                new_move_id = moves_df['Move_ID'].max() + 1 if not moves_df.empty else 1
                new_row = {
                    'Move_ID': new_move_id,
                    'Miscrit_ID': miscrit_id,
                    **{k: new_move[k] for k in required_keys}
                }
                moves_df.loc[len(moves_df)] = new_row
                print(f" + Added move: {new_move['Move_Name']}")

    # Save after all crit_ids are processed
    miscrit_df.to_csv(miscrit_path, index=False)
    moves_df.to_csv(moves_path, index=False)
    print("\n[INFO] Miscrit and Moves data saved.")

if __name__ == "__main__":
    crit_ids = miscrit_id_finder(miscrits)
    miscrit_updater(crit_ids)
