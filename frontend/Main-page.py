import streamlit as st
import os

# Adquiring relative path of this file
path = os.path.dirname(__file__)
# Path to image
path_to_olimpics_logo = os.path.join(path, '..','olympics_folder','documents', 'olympics_logo.png')
st.markdown("""
    #        Welcome to the Olympic App """)

st.image(path_to_olimpics_logo,width=50, use_container_width=True)

st.markdown("""

    ## Where you can find and play with **information** and **results** from different editions and athlets from *1896* till *2022*

""")
