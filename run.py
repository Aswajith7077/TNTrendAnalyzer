import streamlit as st
from app import app
from results import results

if __name__=='__main__':
    page = st.navigation([st.Page(app),st.Page(results)])
    page.run()