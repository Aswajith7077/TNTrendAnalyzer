import numpy as np

import pandas




# Generate 214 random growth rates between -10 and 10
growth_rates = np.random.uniform(0, 1, 20020)

# Convert to a list and print
growth_rates_list = growth_rates.tolist()
print(growth_rates_list)





path = './../data/A-1_NO_OF_VILLAGES_TOWNS_HOUSEHOLDS_POPULATION_AND_AREA_1.xlsx'


pop_data = pandas.read_excel(path)

print(pop_data.shape)


pop_data['GROWTH RATE'] = growth_rates


pop_data = pop_data[pop_data[1] == 33][pop_data[6] == 'Total'][pop_data[4] == 'SUB-DISTRICT']
pop_data = pop_data.drop(columns = [1,4,6,7,8,9,10,12,13,'13.1',14])[1:].sort_values(by = 3).iloc[:-1,:]
print(pop_data.head())

# with pandas.ExcelWriter(path) as writer:
#     pop_data.to_excel(writer,sheet_name = 'Sheet1')





