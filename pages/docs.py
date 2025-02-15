import streamlit as st


def Documentation():

    st.markdown('''
    # Tamil Nadu Trend Analyzer

## Overview

A **Streamlit-based web application** designed to visualize and predict population growth in Tamil Nadu sub-districts using a **continuous-time logistic model**. The app provides a user-friendly interface for analyzing population growth and future infrastructure requirements based on dynamic inputs.

The app integrates map visualization using **Folium**, enabling users to interact with geospatial data and mark specific locations for further analysis.

---

## Features

1. **Population Prediction:**
   - Predicts future population using a continuous-time logistic growth model.
   - Includes sinusoidal adjustments for seasonal variations.

2. **Map Visualization:**
   - Displays Tamil Nadu districts and sub-districts on an interactive map.
   - Allows users to add markers for selected sub-districts.

3. **Dynamic Input Options:**
   - Select a district and sub-districts for analysis.
   - Customize growth model parameters such as time period, amplitude, and sinusoidal components.

4. **Infrastructure Requirements:**
   - Analyzes predicted population to suggest future infrastructure needs, such as:
     - Hospitality
     - Education
     - Public Safety
     - Transportation
     - Water Connection
     - Infrastructures
     - Commercial and Retail

5. **User Interaction:**
   - Provides actionable suggestions for infrastructure needs based on population predictions.
   - Interactive buttons to visualize recommendations for specific facilities.

6. **Data Display:**
   - Show underlying data in tabular format for transparency.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Aswajith7077/PopulationAnalysis.git
   cd PopulationAnalysis
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run run.py
   ```

---

## Usage

1. **Data Requirements:**
   - Ensure the following files are present:
     - GeoJSON to CSV data: `geojson-to-csv.csv`
     - Population data: `A-1_NO_OF_VILLAGES_TOWNS_HOUSEHOLDS_POPULATION_AND_AREA_1.xlsx`

2. **Steps to Use the App:**
   - Select a district from the dropdown.
   - Choose sub-districts for analysis.
   - Adjust growth model parameters (time, amplitude, sinusoidal period) as needed.
   - View predictions and suggested infrastructure needs.

3. **Map Features:**
   - Markers for selected sub-districts.
   - Use the **"Submit"** button to calculate predictions and display results.

4. **Threshold Analysis:**
   - Facilities are suggested based on population thresholds for sub-districts.

---

## File Descriptions

1. **`algo.py`:**
   - Contains the `project_continuous_time_logistic_model` function for population prediction.

2. **`geojson-to-csv.csv`:**
   - GeoJSON data converted to CSV format containing geospatial and demographic details.

3. **`A-1_NO_OF_VILLAGES_TOWNS_HOUSEHOLDS_POPULATION_AND_AREA_1.xlsx`:**
   - Excel file with population data for Tamil Nadu.

---

## Key Functions

1. **Population Prediction:**
   - Uses the logistic model with optional sinusoidal adjustments.

2. **Interactive Map:**
   - Displays sub-districts and allows marker placement.

3. **Threshold Analysis:**
   - Maps population values to predefined facility needs.

4. **Infrastructure Voting:**
   - Users can interact with infrastructure recommendations via dialog boxes.

---

## Dependencies

- **Streamlit**: For creating the web interface.
- **Folium**: For map visualization.
- **Pandas**: For data manipulation.
- **Shapely**: For handling geospatial data.
- **NumPy**: For numerical calculations.
- **Math**: For mathematical computations.

---

## Future Improvements

- Add support for uploading custom datasets.
- Improve map interactivity with detailed overlays.
- Include more advanced prediction models.
- Optimize the interface for better user experience.

---

''')