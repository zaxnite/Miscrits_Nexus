import pandas as pd

df = pd.read_csv('D:/miscrits_nexus/data/miscrit_database.csv')

print(df[df['Miscrit_ID'] == 98].index
)