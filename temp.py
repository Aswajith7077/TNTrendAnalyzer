
import pandas



fileName = 'C:\\Users\\ASWAJITH\\OneDrive\ドキュメント\\SCL_Package\\geojson-to-csv.csv'
data = pandas.read_csv(fileName).sort_values(by = 'dtcode11').iloc[1:-1,:]

path = './A-1_NO_OF_VILLAGES_TOWNS_HOUSEHOLDS_POPULATION_AND_AREA_1.xlsx'


pop_data = pandas.read_excel(path)
pop_data = pop_data[pop_data[1] == 33][pop_data[6] == 'Total'][pop_data[4] == 'SUB-DISTRICT']
pop_data = pop_data.drop(columns = [1,4,6,7,8,9,10,12,13,'13.1',14])[1:].sort_values(by = 3).iloc[:-1,:]


data['POPULATION'] = pop_data[11].values


print(pop_data[11])

# print(pop_data[5] - set(pop_data[5]))
print(pop_data[5].duplicated().shape)


# for i in pop_data[3]:

#     if i in data['stdcode11']:




pop_data[3] = pandas.to_numeric(pop_data[3])

print(pop_data)
print(data)

# print(pop_data.shape)
# print(pop_data)

# print(pop_data[pop_data[3] == '05694'])


print()







