import streamlit as st
import numpy as np
import pandas
import folium
from streamlit_folium import st_folium
from shapely.geometry import Polygon
from shapely import wkt
from src.algo import project_continuous_time_logistic_model
import math





class FileHandler:

    TamilNaduLocation = 11.127123, 78.656891
    facilities = ['Hospitality','Education','Public Safety','Transportation','Water Connection','Infrastructures','Commercial and Retail']
    icons = ['hospital','school','police','train','water','tower','business']

    def __init__(self):
        self.fileName = 'C:\\Users\\ASWAJITH\\OneDrive\\ドキュメント\\SCL_Package\\geojson-to-csv.csv'
        self.data = pandas.read_csv(self.fileName).sort_values(by = 'dtcode11').iloc[1:-1,:]
        self.path = './A-1_NO_OF_VILLAGES_TOWNS_HOUSEHOLDS_POPULATION_AND_AREA_1.xlsx'

        self.pop_data = pandas.read_excel(self.path)
        self.pop_data = self.pop_data[self.pop_data[1] == 33][self.pop_data[6] == 'Total'][self.pop_data[4] == 'SUB-DISTRICT']
        self.pop_data = self.pop_data.drop(columns = [1,4,6,7,8,9,10,12,13,'13.1',14])[1:].sort_values(by = 3).iloc[:-1,:]

        self.data['POPULATION'] = self.pop_data[11].values
        self.data['GROWTH RATE'] = self.pop_data['GROWTH RATE'].values / 100



# class FacilityComputation:

    



class ApplicationUtilities:

    def __init__(self):

        self.fh = FileHandler()

        if 'map_object' not in st.session_state:
            st.session_state.map_object = folium.Map(location=(11.127123, 78.656891), zoom_start=7)
        if 'values' not in st.session_state:
            st.session_state.values = []
        if 'final_population' not in st.session_state:
            st.session_state.final_population = []

    @st.cache_data  
    def write(temp:list):
        for i in temp:
            st.write(i)
  
    def threshold(self,fac_index,final,pop,dist):
        temp = [[] for i in range(len(FileHandler.facilities))]
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

    def addMarker(self):
    # Reset the map to clear existing markers
        st.session_state.map_object = folium.Map(location=FileHandler.TamilNaduLocation, zoom_start=7)

        # Add markers based on selected sub-districts
        for i in st.session_state['values']:
            value = self.fh.data[self.fh.data['sdtname'] == i]['wkt']
            current = wkt.loads(value.values[0])

            location = list(current.centroid.coords[0])[::-1]
            folium.Marker(location=location,popup = i).add_to(st.session_state.map_object)



isMarkerAdded = False
isUpdateNeeded = False






@st.cache_data  
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







def app():

    util = ApplicationUtilities()
    # data = pandas.read_csv(fileName).sort_values(by = 'dtcode11')
   
    st.title('Population Prediction using Continuous Time Logistic Model')
    st.markdown('\n\n\n')
    st.markdown('\n\n\n')


    districts = set(util.fh.data['dtname'])
    print(util.fh)

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
            util.fh.data.loc[util.fh.data['dtname'] == selected_district]['sdtname'],
            key='values',
            on_change= util.addMarker  # Call addMarker each time selection changes
        )

        c1,c2 = st.columns([5,5])
        time = c1.slider('Select the Time ',min_value = 0,max_value = 100)
        time = c1.number_input('Select the Time',value = 50)
        k1 = c2.number_input('Select the Amplitude',value = 100)
        tp = st.number_input('Select the time period for sinusoid',value = 15.5)
        canModify = st.selectbox(
            'Can we modify the parameters ? ',
            ['No','Yes'],
        )

        # print(util.fh.data)


        st.markdown('')
        canModify = True if(canModify.lower() == 'yes') else False
        
        
        # print(selected_subdistricts)
        if selected_subdistricts and st.button('Submit',use_container_width = True,type='primary'):
            populations = []
            final_population = []
            for subdistrict in selected_subdistricts:

                print('\n\n\n\n\n\n\n\n\n')
                value = util.fh.data[util.fh.data['sdtname'] == subdistrict]
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
                for i in range(len(FileHandler.facilities)):
                    # print('Final : ',final_population)
                    # print('Current : ',populations)
                    result = util.threshold(i,final_population,populations,list(selected_subdistricts))
                    # if not result:
                    #     a,b = None,None
                    # else:
                    #     a,b = result
                    print('Result : ',result)
                    st.button(f'{FileHandler.facilities[i]}',use_container_width = True,on_click = vote,args = (result[:][0],np.unique(result[i][1])))
                        
  
                        

        
    with col2:

        st_folium(st.session_state.map_object,use_container_width = True)        
        with st.expander("Show Data Frame"):
            st.dataframe(data = util.fh.data,use_container_width = True)
        