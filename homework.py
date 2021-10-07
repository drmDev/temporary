import pandas as pd             # pip install pandas
import numpy as np              # pip install numpy
from datetime import timedelta

# Read the dataset
data = pd.read_csv('weather_mod.csv', parse_dates=['date'])

# Print missing dates
date_fmt = "%Y-%m-%d"  # yyyy-mm-dd
missing_days = []
start_idx = 0

for day_idx in range(start_idx, len(data)):
    # cannot calculate the previous date on the first iteration
    if day_idx != start_idx:
        curr_dt = data.date[day_idx]
        prev_dt = data.date[day_idx - 1]
        day_diff = (curr_dt - prev_dt).days
        
        # more than 1 days means there is a missing date
        if day_diff > 1:
            # append to list of missing dates from the range of days between the current and previous dates found
            for days_back in range(1, day_diff):
                md = prev_dt + timedelta(days=days_back)
                formatted_md = md.strftime(date_fmt)
                missing_days.append(formatted_md)

assert(len(missing_days) == 6)
print("Missing days: ", missing_days)

# Find dates with incorrect mean values
invalid_mean_days = []
for _, day in data.iterrows():
    min_temp = day['actual_min_temp']
    max_temp = day['actual_max_temp']
    
    # get current mean and compare to actual mean calculated (use ceiling for rounding)
    curr_mean = day['actual_mean_temp']
    act_mean = np.ceil(np.mean([min_temp, max_temp]))
    
    # incorrect mean value found, format the date and add to the invalid list
    if curr_mean != act_mean:
        day_formatted = day['date'].strftime(date_fmt)
        invalid_mean_days.append(day_formatted)

assert(len(invalid_mean_days) == 2)
print("Invalid mean for days:", invalid_mean_days)
