import pandas as pd

'''
to be deleted when everything is done, I'm just using it to the check the data types and the nan values in all csv files
+ print the markdown table
'''

path = 'stimuli/aoi_texts/aoi/b2.ias'

csv = pd.read_csv(path, sep='\s+')

cols = [c for c in csv.columns]

new_df = pd.DataFrame({'Column': cols, 'Data type': [dt for dt in csv.dtypes], 'Description': [pd.NA for c in cols]})

print(new_df.to_markdown(index=False))



