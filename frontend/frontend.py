import streamlit as st
import os

st.markdown("""
    # Welcome to the Olympics App

    ## Where you can find and play with **information** and **results** from different editions and athlets from *1896* till *2022*

""")

# Adquiring relative path of this file
path = os.path.dirname(__file__)
# Path to image
path_to_olimpics_logo = os.path.join(path, '..','olympics_folder','documents', 'olympics_logo.png')

st.image(path_to_olimpics_logo,width=50, use_container_width=True)
