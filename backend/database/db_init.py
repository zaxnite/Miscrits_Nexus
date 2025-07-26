from sqlalchemy import create_engine
import pandas as pd

# File paths
miscrit_path = r'D:\miscrits_nexus\data\miscrit_database.csv'
moves_path = r'D:\miscrits_nexus\data\moves_database.csv'

# Read CSVs
miscrit_df = pd.read_csv(miscrit_path)
moves_df = pd.read_csv(moves_path)

# Create SQLite engine — specify output location
engine = create_engine(r"sqlite:///D:/miscrits_nexus/data/miscrit_data.db")

# Write to SQL without including DataFrame index
miscrit_df.to_sql("miscrits", engine, index=False, if_exists="replace")
moves_df.to_sql("moves", engine, index=False, if_exists="replace")
