import pandas as pd
import json

data = []

files =['dive_ni.json', 
        'diventures.json', 
        'ocascuba.json', 
        'diving_ie.json', 
        'dive_centers_worldwide.json', 
        'bsac.json', 
        'BCDivingClubs.json', 
        'mlssa.json', 
        'aquanaut.json', 
        'diveguide.json', 
        'nabs_divers.json', 
        'underwater.json',
        'divescover_canada.json',
        'divescover_Mexico.json',
        'divescover_USA.json']

for file in files:
    f = open(file)
    d = json.load(f)
    data.extend(d)

print(f'Number of records: {len(data)}')

country_df = {}

for d in data:
    if d['country'] is not None:
        key = d['country'].strip()
    else:
        key = d['country']
        
    if key not in country_df:
        country_df[key] = []
        
    country_df[key].append(d)
	
empty_emails = 0

with pd.ExcelWriter('Dive Clubs Info.xlsx') as writer:
    if None in country_df.keys():
        df = pd.DataFrame.from_dict(country_df[None])
        df[['club_name', 'city', 'building', 'country', 'contact', 'phone', 'email']].to_excel(writer, sheet_name = 'UNKNOWN', index=False)
        empty_emails+=len(df[df['email'].isna()])
        del country_df[None]

    for key in sorted(list(country_df.keys())):
        if key is None or key == 'None':
             sheet_name = 'UNKNOWN'
        elif key == 'UK/England' or key == 'UK/Wales' or key == 'United Kingdom' or key == 'London':
            sheet_name = 'UK'
        elif '/' in key:
            sheet_name = key.split('/')[0]
        elif key == 'Maledives':
            sheet_name = 'Maldives'
        elif key == 'Polen':
            sheet_name = 'Poland'
        elif key == 'Slovenija':
            sheet_name = 'Slovenia'
        else:
            sheet_name = key.strip()
            
        df = pd.DataFrame.from_dict(country_df[key])
        empty_emails+=len(df[df['email'].isna()])
        df[['club_name', 'city', 'building', 'country', 'contact', 'phone', 'email']].to_excel(writer, sheet_name=sheet_name, index=False)

print('Number of missing emails: ', empty_emails)