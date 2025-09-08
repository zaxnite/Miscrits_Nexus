from sqlalchemy import create_engine
import pandas as pd
from rich.console import Console
from rich.table import Table

# Setup console
console = Console()

# Connect to the SQLite file
engine = create_engine(r"sqlite:///D:/miscrits_nexus/data/miscrit_data.db")

# Function to pretty-print DataFrame using rich
def print_rich_table(df, title, max_rows=10):
    table = Table(title=title)

    # Add only first max_cols columns
    columns = df.columns
    for col in columns:
        table.add_column(col, header_style='cyan')

    # Add up to max_rows rows
    for _, row in df.head(max_rows).iterrows():
        table.add_row(*[str(row[col]) for col in columns], style="green")

    console.print(table)


# Read 'miscrits' table
miscrit_df = pd.read_sql("SELECT * FROM miscrits LIMIT 5", engine)
print_rich_table(miscrit_df, "Miscrit Database")

# Read 'moves' table
moves_df = pd.read_sql("SELECT * FROM moves LIMIT 5", engine)
print_rich_table(moves_df, "Moves Database")

relics_df = pd.read_sql("SELECT * FROM relics LIMIT 5", engine)
print_rich_table(relics_df, "Relics Database")