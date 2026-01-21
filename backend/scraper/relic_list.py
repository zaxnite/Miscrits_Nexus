import pandas as pd

relics_df = pd.read_csv(r'D:\miscrits_nexus\data\miscrit_relics.csv',index_col="ID")

# Get a random row for verification purposes
random_row = relics_df.sample(n=1)
print("Random relic for verification:")
print(random_row)

