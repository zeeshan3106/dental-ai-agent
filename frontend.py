import streamlit as st
import requests 
import json

API = "http://127.0.0.1:8000/Dental"
st.title("Dental Agent")

input = st.text_input("Enter")

if st.button("Enter"):
    res = requests.post(API,input)
    st.write(res.json())

