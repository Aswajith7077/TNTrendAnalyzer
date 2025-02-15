import streamlit as st
import numpy as np
import pandas
import folium
from streamlit_folium import st_folium
from shapely.geometry import Polygon
from shapely import wkt
from algo import project_continuous_time_logistic_model
import math


fileName = 'C:\\Users\\ASWAJITH\\OneDrive\\ドキュメント\\SCL_Package\\geojson-to-csv.csv'
data = pandas.read_csv(fileName).sort_values(by = 'dtcode11').iloc[1:-1,:]

path = './A-1_NO_OF_VILLAGES_TOWNS_HOUSEHOLDS_POPULATION_AND_AREA_1.xlsx'


pop_data = pandas.read_excel(path)
pop_data = pop_data[pop_data[1] == 33][pop_data[6] == 'Total'][pop_data[4] == 'SUB-DISTRICT']
pop_data = pop_data.drop(columns = [1,4,6,7,8,9,10,12,13,'13.1',14])[1:].sort_values(by = 3).iloc[:-1,:]

data['POPULATION'] = pop_data[11].values
data['GROWTH RATE'] = pop_data['GROWTH RATE'].values / 100


facilities = ['Hospitality','Education','Public Safety','Transportation','Water Connection','Infrastructures','Commercial and Retail']
icons = ['hospital','school','police','train','water','tower','business']





isMarkerAdded = False
isUpdateNeeded = False


if 'map_object' not in st.session_state:
    st.session_state.map_object = folium.Map(location=(11.127123, 78.656891), zoom_start=7)
if 'values' not in st.session_state:
    st.session_state.values = []
if 'final_population' not in st.session_state:
    st.session_state.final_population = []

def write(temp:list):
    for i in temp:
        st.write(i)


@st.dialog("Facility")
def vote(final_pop,dist):
    print('voted')

    if dist is None or final_pop is None:
        st.write('No Future requirements needed!')
        return

    i = 0
    for i in range(len(dist)):
        c1,s,c2 = st.columns([3,4,7])
        c1.write(f'\t{i + 1}.\t{dist}')
        c2.write(f'{final_pop}')

    if st.button("OK",use_container_width = True):

        st.session_state.show_dialog = False  # Close the dialog after voting
        st.rerun()

def threshold(fac_index,final,pop,dist):
    temp = [[]] * len(facilities)
    print('Threshold')

    print(len(final))
    print(len(pop))

    for i in range(len(pop)):
        v = final[i]
        print("V : ",v)
        if 12000 <= v :
            temp[1].append([final[i],dist[i]])
        if 200000 <= v:# and v <= 30000:
            temp[0].append([final[i],dist[i]])
        if 500000 <= v:#and v <= 100000:
            temp[2].append([final[i],dist[i]])
        if v <= 50000:
            temp[3].append([final[i],dist[i]])
        if 100000 <= v:
            temp[4].append([final[i],dist])
        if 2000000 <= v:
            temp[-2].append([final[i],dist[i]])
        if 3000000 <= v:
            temp[-1].append([final[i],dist[i]])

        print('Temp : ',temp)

    return temp[fac_index]

def addMarker():
    # Reset the map to clear existing markers
    st.session_state.map_object = folium.Map(location=(11.127123, 78.656891), zoom_start=7)

    # Add markers based on selected sub-districts
    for i in st.session_state['values']:
        value = data[data['sdtname'] == i]['wkt']
        current = wkt.loads(value.values[0])

        location = list(current.centroid.coords[0])[::-1]
        folium.Marker(location=location,popup = i).add_to(st.session_state.map_object)

def app():

    # data = pandas.read_csv(fileName).sort_values(by = 'dtcode11')
   
    st.title('Population Prediction using Continuous Time Logistic Model')
    st.markdown('\n\n\n')
    st.markdown('\n\n\n')


    districts = set(data['dtname'])
    print(data.shape)

    col1,spacer,col2 = st.columns([3.5,0.5,6.5])
    
    

    with col1:
        selected_district = st.selectbox(
            "Select a District",
            districts
        )
        if 'values' not in st.session_state:
            st.session_state.values = []


        selected_subdistricts = st.multiselect(
            "Choose the Sub District",
            data.loc[data['dtname'] == selected_district]['sdtname'],
            key='values',
            on_change=addMarker  # Call addMarker each time selection changes
        )

        c1,c2 = st.columns([5,5])
        time = c1.number_input('Select the Time',value = 50)
        k1 = c2.number_input('Select the Amplitude',value = 100)
        tp = st.number_input('Select the time period for sinusoid',value = 15.5)
        canModify = st.selectbox(
            'Can we modify the parameters ? ',
            ['No','Yes'],
        )

        # print(data)


        st.markdown('')
        canModify = True if(canModify.lower() == 'yes') else False
        
        
        # print(selected_subdistricts)
        if selected_subdistricts and st.button('Submit',use_container_width = True,type='primary'):
            populations = []
            final_population = []
            for subdistrict in selected_subdistricts:

                print('\n\n\n\n\n\n\n\n\n')
                value = data[data['sdtname'] == subdistrict]
                population = value['POPULATION'].values[0]
                populations.append(population)
                growth_rate = np.abs(value['GROWTH RATE'].values[0])

                final_pop = project_continuous_time_logistic_model(
                    init_pop = population,
                    time_to_run = time,
                    r = growth_rate * 100, 
                    k = population * 1.4543875,
                    sinusoid = True,
                    sinusoid_k0 = population,
                    sinusoid_k1 = k1,
                    sinusoid_tp = tp,
                    modify_initial_pop = canModify,
                    modify_k_values = False,
                    modify_r_value = canModify,
                    modify_tp_value = canModify
                )
                final_population.append(final_pop)

                # print(population,growth_rate)
            print(final_population)

            # buttons = []
        
            container = st.container(height = 400)
            with container:
                for i in range(len(facilities)):
                    # print('Final : ',final_population)
                    # print('Current : ',populations)
                    result = threshold(i,final_population,populations,list(selected_subdistricts))
                    # if not result:
                    #     a,b = None,None
                    # else:
                    #     a,b = result
                    print('Result : ',result)
                    st.button(f'{facilities[i]}',use_container_width = True,on_click = vote,args = (result[:][0],np.unique(result[i][1])))
                        
  
                        

        
    with col2:

        st_folium(st.session_state.map_object,use_container_width = True)        
        
        