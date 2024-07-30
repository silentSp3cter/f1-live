from urllib.request import urlopen
import json
import pandas as pd

# input_string = str(input('GP; Year; Session; Seperate with ;'))
input_string = 'Silverstone; 2024;Race'
gp = input_string.split(";")[0].strip()
year = input_string.split(";")[1].strip()
session = input_string.split(";")[2].strip()
print(gp, year, session)

'''Get session key'''
response = urlopen(f'https://api.openf1.org/v1/sessions?location={gp}&year={year}&session_name={session}')
data = json.loads(response.read().decode('utf-8'))
session_key = data[0]['session_key']

'''Get grid'''
response = urlopen(f'https://api.openf1.org/v1/drivers?session_key={session_key}')
drivers = json.loads(response.read().decode('utf-8'))
grid = pd.json_normalize(drivers)
grid = grid[['session_key', 'team_name', 'name_acronym', 'driver_number', 'broadcast_name']]

'''Position data'''
response = urlopen(f'https://api.openf1.org/v1/position?session_key={session_key}')
pos_response = json.loads(response.read().decode('utf-8'))
pos = pd.json_normalize(pos_response)
pos['date'] = pd.to_datetime(pos['date'])
idx = pos.groupby('driver_number')['date'].idxmax()
pos = pos.loc[idx]
pos = pos.sort_values(by=['position'], ascending=True)
pos = pos[['driver_number', 'position']]
grid = pd.merge(grid, pos, on=['driver_number'], how='left', suffixes=(None, '_right1'))

'''Lap data'''
response = urlopen(f'https://api.openf1.org/v1/laps?session_key={session_key}')
lap_response = json.loads(response.read().decode('utf-8'))
lap = pd.json_normalize(lap_response)
lap['date_start'] = pd.to_datetime(lap['date_start'], format='ISO8601')
idx = lap.groupby('driver_number')['date_start'].idxmax()
lap = lap.loc[idx]
lap = lap[['session_key', 'driver_number', 'i1_speed', 'i2_speed',
           'st_speed', 'date_start', 'lap_duration', 'is_pit_out_lap',
           'duration_sector_1', 'duration_sector_2', 'duration_sector_3',
           'segments_sector_1', 'segments_sector_2', 'segments_sector_3',
           'lap_number']]
grid = pd.merge(grid, lap, on=['driver_number'], how='left', suffixes=(None, '_right2'))
grid = grid.sort_values(by=['position'], ascending=True)

print()