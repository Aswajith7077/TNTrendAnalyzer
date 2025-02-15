import streamlit as st
import plotly.express as px
import pandas
import numpy

fileName = 'data/geojson-to-csv.csv'
path = 'data/A-1_NO_OF_VILLAGES_TOWNS_HOUSEHOLDS_POPULATION_AND_AREA_1.xlsx'


data = pandas.read_csv(fileName).sort_values(by = 'dtcode11').iloc[1:-1,:]
pop_data = pandas.read_excel(path)

# sub_district_pop = pop_data[pop_data[1] == 33][pop_data[6] == 'Total'][pop_data[4] == 'DISTRICT']
# print(sub_district_pop.head())


district_pop = pop_data[pop_data[1] == 33][pop_data[6] == 'Total'][pop_data[4] == 'DISTRICT']
district_pop = district_pop.drop(columns = [1,4,6,7,8,9,10,12,13,'13.1',14])[1:].sort_values(by = 3).iloc[:-1,:]



district_pop_map = {}
district_code_map = {}

for ind,val in district_pop.iterrows():
    district_pop_map[val[5]] = val[11]
    district_code_map[val[5]] = val[2]

# for ind,val in district_pop.iterrows():
    



pop_data = pop_data[pop_data[1] == 33][pop_data[6] == 'Total'][pop_data[4] == 'SUB-DISTRICT']
pop_data = pop_data.drop(columns = [1,4,6,7,8,9,10,12,13,'13.1',14])[1:].sort_values(by = 3).iloc[:-1,:]


def getDistrictCode(district):

    code = -1 

    if district in district_code_map:
        code = district_code_map[district]

    return code


def getSubPopulation(district):

    code = getDistrictCode(district = district)

    result = {}

    print(code,type(code))
    for ind,val in pop_data.iterrows():
        # print(val[2],code,type(val[2]))
        if val[2] == code:
            result[val[5]] = val[11]

    df = pandas.DataFrame()
    df['region'] = numpy.array(list(result.keys()))
    df['population'] = numpy.array(list(result.values()))

    print('DF',df)

    return df



def getDistrictPopulation(district):

    if district in district_pop_map:
        return district_pop_map[district]
    return -1


def Visualizations():
    # with st.expander("Show Data Frame"):
    st.header("Results")
    st.write('Data Frame of the districts and sub-districts')
    st.dataframe(data = data,use_container_width = True)

    st.write('Data Frame of population on each districts')
    st.dataframe(data = pop_data,use_container_width = True)

    # getDistrictPopulation()

    st.header('Population Visualization for each district')
    st.write(' ')
    st.bar_chart(pandas.Series(district_pop_map),color=["#8800F0"])


    col1,col2 = st.columns(2)
    with col1:
        d = st.selectbox("District wise Population distribution",tuple(district_pop_map.keys())[1:])
        dat = getSubPopulation(d)
        chart = px.pie(dat,values = 'population',names = 'region')
        st.plotly_chart(chart)
    
    with col2:
        d = st.selectbox("District Area",tuple(district_pop_map.keys()))
        
        # st.plotly_chart(chart)

    st.write('No Results found')


