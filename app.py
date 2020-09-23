import streamlit as st 
from economics import Economics
import pandas as pd
import io

#streamlit settings 
# st.set_option('deprecation.showfileUploaderEncoding', False)

# functions
@st.cache(persist=True)
def file_uploder(path):
    df = pd.read_csv(path)
    return df
# my model 
eco = Economics()

# Global Variable
features = ['Demand and Supply']

# streamlt
st.title("Economics Model By Ahmed Maher")
selected_features = st.multiselect('Apps or Features that you Want' , features)

    #'Demand and Supply'
if features[0] in selected_features:
    st.header(features[0])
    st.sidebar.header(features[0])
    st.sidebar.markdown('type number of precent in a fraction format ex:instead of "1%" type as 0.01 ')
    shift_demand_curve = st.sidebar.number_input('Change demand by %' , 0.0)
    shift_supply_curve = st.sidebar.number_input('Change supply by %' , 0.0)
    if st.sidebar.checkbox('Do you Want to upload your own data?' , False):
        DS_data_uploader = st.sidebar.file_uploader('upload your data here in csv format' )
        DS_Default_Header = {'price':'price' , 'Demand':'Demand' , 'Supply':'Supply'}
        if st.sidebar.checkbox('Change Defalut header' , False):
            for key , val in DS_Default_Header.items():
                DS_Default_Header[key] = st.sidebar.text_input('Change {} header to:'.format(key) , val , key='DS_Default_Header_{}'.format(key))

        if st.sidebar.button('run'):
            DS_data = file_uploder(DS_data_uploader)
            st.pyplot(eco.demand_supply_cruve(data=DS_data, header=DS_Default_Header , shift_demand_curve=shift_demand_curve , shift_supply_curve=shift_supply_curve))
    else:
        st.pyplot(eco.demand_supply_cruve(shift_demand_curve=shift_demand_curve , shift_supply_curve=shift_supply_curve))
    st.info('Note: Market equilibrium exists, when quantity demanded equals quantity supplied')