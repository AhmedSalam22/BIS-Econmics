import streamlit as st 
from economics import Economics
import pandas as pd
import time
#streamlit settings 
st.set_option('deprecation.showfileUploaderEncoding', False)

# functions
def file_uploder(path):
    df = pd.read_csv(path , sep=';')
    return df


def header(num_feature):
    st.header(features[num_feature])
    st.sidebar.header(features[num_feature])

def do_something_in_sidebar_True(num_feature , data  ,Default_Header):
    if num_feature == 0:
        st.pyplot(eco.demand_supply_cruve(data=data, header=Default_Header , shift_demand_curve=shift_demand_curve , shift_supply_curve=shift_supply_curve))

def do_something_in_sidebar_False(num_feature):
    if num_feature == 0:#'Demand and Supply'
        st.pyplot(eco.demand_supply_cruve(shift_demand_curve=shift_demand_curve , shift_supply_curve=shift_supply_curve))
    elif num_feature==1: #'Marginal utility and total utility'
        data =  {'quantity':list(range(1,7)) ,'Total utility':[20,36,46,52,54,52]}
        data = pd.DataFrame(data)
        st.text("""For example, suppose you are very hungry. You decide to eat pizza. The first slice
of pizza gives you 20 units of utility. After eating the first slice, you decide to have
the second slice. The satisfaction you receive from the two slices is 36. Three
slices give you 46 units of utility. This table shows the total utility. Estimate MU.""")
        if st.checkbox("Show example data", False):
            st.dataframe(data)
        fig , consumer_equilibrium , consumer_surplus = eco.marginal_utility(price=price)
        st.markdown("consumer equilibrium = `{}` when price = `{}`".format(consumer_equilibrium , price))
        st.markdown("consumer surplus = `{}` when price = `{}`".format(consumer_surplus , price))
        st.pyplot(fig)

def sidebar(num_feature , Default_Header ):
    if st.sidebar.checkbox('Do you Want to upload your own data?' , False  , key='chk_'+features[num_feature]):
        data_uploader = st.sidebar.file_uploader('upload your data here in csv format', type="csv" , key='file_'+features[num_feature])
        if st.sidebar.checkbox('Change Defalut header' , False , key='chk_H'+features[num_feature] ):
            for key , val in Default_Header.items():
                Default_Header[key] = st.sidebar.text_input('Change {} header to:'.format(key) , val , key='Default_Header_{}_{}'.format(key, num_feature))
        show_raw=st.sidebar.checkbox('Show raw data' , key=str(num_feature))
        if st.sidebar.checkbox('Run' , key=str(num_feature)):
            time.sleep(5)
            data = file_uploder(data_uploader)
            if show_raw:
                st.dataframe(data)
            do_something_in_sidebar_True(num_feature , data , Default_Header)
    else:
        time.sleep(5)
        do_something_in_sidebar_False(num_feature)
# my model 
eco = Economics()

# Global Variable
features = ['Demand and Supply',
            'Marginal utility and total utility',
            ]

# streamlt
st.title("Economics Model By Ahmed Maher")
selected_features = st.multiselect('Apps or Features that you Want' , features)

    #'Demand and Supply'
if features[0] in selected_features:
    header(0)
    st.sidebar.markdown('type number of precent in a fraction format ex:instead of "1%" type as 0.01 ')
    shift_demand_curve = st.sidebar.number_input('Change demand by %')
    shift_supply_curve = st.sidebar.number_input('Change supply by %')
    sidebar(0 , {'price':'price' , 'Demand':'Demand' , 'Supply':'Supply'})
    st.info('Note: Market equilibrium exists, when quantity demanded equals quantity supplied')

if features[1] in selected_features:
    header(1)
    price = st.number_input("price number", 0.0)

    sidebar(1 , {'quantity':'quantity' , 'Total utility':'Total utility'})

    st.subheader('consumer equilibrium?' )
    st.info('Consumer equilibrium exists when the price equals the marginal utility.')
    # st.text("If the price is $x. what is the consumer equilibrium? ")
    st.subheader("Consumer surplus?")
    st.info("""• Consumer surplus: can be measured by the area under demand curve
(marginal utility curve) and above the price of good""")