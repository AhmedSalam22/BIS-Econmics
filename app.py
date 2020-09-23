import streamlit as st 
from economics import Economics
st.title("Eco")
eco = Economics()
st.pyplot(eco.demand_supply_cruve())