import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

"""
Datasets
https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv - temperatures
http://api.worldbank.org/v2/en/indicator/EN.ATM.CO2E.PC?downloadformat=csv - co2 levels
"""

df_gtemp = pd.read_csv(r'path_to_csv_file\global_temp.csv', skiprows=1)
df_co2 = pd.read_csv(r'path_to_csv_file\API_co2.csv', skiprows=4)

# Cleaning dataframes
df_gtemp.set_index('Year', inplace=True)
df1_temp = df_gtemp.iloc[80:135, 5:6]
df1_temp = pd.DataFrame(df1_temp['Jun'])

df1_co2 = df_co2.iloc[0:, 4:59]
df1_co2.fillna(0, inplace=True)
df1_co2 = df1_co2.T
df1_co2['total_emissions'] = df1_co2[list(df1_co2.columns)].sum(axis=1)
df1_co2.index.names = ['Year']
df1_co2 = pd.DataFrame(df1_co2['total_emissions'])

df1_temp.reset_index(inplace=True)
df1_co2.reset_index(inplace=True)

df1_co2['Year'] = df1_co2['Year'].astype(int)

df_merged = pd.merge(df1_temp, df1_co2, how='outer', left_index=True, right_index=True)
df_merged.drop(['Year_x'], axis=1, inplace=True)
df_merged.set_index('Year_y', inplace=True)

# Graph plotting
sns.set_style('darkgrid')

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Time')
ax1.set_ylabel('Global CO2 emissions (Metric tons)', color=color)
ax1.plot(df_merged.index, df_merged['total_emissions'], color=color, marker='o', label='CO2 Emissions')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # Second axes shared with first
color = 'tab:blue'
ax2.set_ylabel('Global temperature change (Deg. celsius)', color=color)
ax2.plot(df_merged.index, df_merged['Jun'], color=color, marker='o', label='Temperature change')
ax2.tick_params(axis='y', labelcolor=color)

plt.title('CO2 Emissions vs Temperature Change')
ax1.legend(loc='upper left')
ax2.legend(loc='upper center')

plt.tight_layout()
plt.show()
