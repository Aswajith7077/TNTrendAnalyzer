import streamlit as st
from pages.predictor import Predictor
from pages.visualizer import Visualizations
from pages.docs import Documentation

if __name__=='__main__':
    
    st.sidebar.markdown("**Tamil Nadu Trend Analyzer**")
    st.sidebar.markdown('''<div style="text-align: justify; padding: 0px 10px 0px 10px"> Our tool tells you about the population growth 2020 to 2023 with fluctuations (Disturances) in the growth of the population.</div>''',unsafe_allow_html=True)
    page = st.navigation([st.Page(Predictor),st.Page(Visualizations),st.Page(Documentation)])
    page.run()