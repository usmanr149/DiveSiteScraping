import pandas as pd
import json

data = []

files = ['aquanaut.json', 
         'diventures.json', 
         'dive_clubs_germany.json',
         'diveguide.json'
         ]

for file in files:
    f = open(file)
    d = json.load(f)
    data.extend(d)

country_df = {}

for d in data:
	if d['country'] not in country_df:
		country_df[d['country']] = []

	country_df[d['country']].append(d)

with pd.ExcelWriter('DATAFILE.xlsx') as writer:  
    for key in country_df.keys():
        if key is None or key == 'None':
             sheet_name = 'UNKNOWN'
        elif key == 'UK/England':
            sheet_name = 'UK'
        elif key == 'UK/Wales':
            sheet_name = 'UK'
        elif '/' in key:
            sheet_name = key.split('/')[0]
        else:
            sheet_name = key
            
        df = pd.DataFrame.from_dict(country_df[key])
        df[['club_name', 'city', 'building', 'country', 'contact', 'phone', 'email']].to_excel(writer, sheet_name=sheet_name, index=False)