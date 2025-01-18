
import streamlit as st
import pandas as pd
import folium
from shapely import wkt
from streamlit_folium import st_folium

# Initialize your map and other session state variables if they don't exist
if 'map_object' not in st.session_state:
    st.session_state.map_object = folium.Map(location=(11.127123, 78.656891), zoom_start=7)
if 'values' not in st.session_state:
    st.session_state.values = []
if 'final_population' not in st.session_state:
    st.session_state.final_population = []

# Load data (example structure; replace with your actual file paths and data)
data = pd.DataFrame({
    'sdtname': ['LocationA', 'LocationB', 'LocationC'],
    'wkt': ['POINT(11.127123 78.656891)', 'POINT(11.027123 78.556891)', 'POINT(11.227123 78.756891)'],
    'dtname': ['District1', 'District1', 'District2']
})

# Define addMarker function to update the map object only
def addMarker():
    # Reset the map to clear existing markers
    st.session_state.map_object = folium.Map(location=(11.127123, 78.656891), zoom_start=7)

    # Add markers based on selected sub-districts
    for i in st.session_state['values']:
        current = wkt.loads(data[data['sdtname'] == i]['wkt'].values[0])
        location = list(current.centroid.coords[0])
        print(location)
        folium.Marker(location=location).add_to(st.session_state.map_object)

# App layout
st.title("Population Prediction using Continuous Time Logistic Model")
col1, col2 = st.columns([3.5, 6.5])

with col1:
    districts = set(data['dtname'])
    selected_district = st.selectbox("Select a District", districts)
    selected_subdistricts = st.multiselect(
        "Choose the Sub District",
        data.loc[data['dtname'] == selected_district]['sdtname'],
        key='values',
        on_change=addMarker  # Call addMarker each time selection changes
    )

# Map rendering in col2
with col2:
    st_folium(st.session_state.map_object, use_container_width=True)
    with st.expander("Show Data Frame"):
        st.dataframe(data, use_container_width=True)
