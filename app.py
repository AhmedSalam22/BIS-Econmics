import streamlit as st 
from economics import Economics
import pandas as pd
import time
#streamlit settings 
st.set_option('deprecation.showfileUploaderEncoding', False)

# functions
@st.cache(persist=True)
def file_uploder(path):
    df = pd.read_csv(path , sep=';')
    return df


def header(num_feature):
    st.header(features[num_feature])
    st.sidebar.header(features[num_feature])

def do_something_in_sidebar_True(num_feature , data  ,Default_Header):
    if num_feature == 0:#'Demand and Supply'
        st.pyplot(eco.demand_supply_cruve(data=data, header=Default_Header , shift_demand_curve=shift_demand_curve , shift_supply_curve=shift_supply_curve))
    elif num_feature == 1:#'Marginal utility and total utility'
        fig , consumer_equilibrium , consumer_surplus = eco.marginal_utility(data=data, header=Default_Header, price=price)
        st.markdown("consumer equilibrium = `{}` when price = `{}`".format(consumer_equilibrium , price))
        st.markdown("consumer surplus = `{}` when price = `{}`".format(consumer_surplus , price))
        st.pyplot(fig)
    elif num_feature == 2:#'Relation between output and labor in short run (holding other inputs fixed (capital and technology
        st.pyplot(eco.relation_between_output_and_labor(data=data , header=Default_Header))
    elif num_feature == 3:
        st.pyplot(eco.average_cost_and_marginal_cost(data=data , header=Default_Header))
    elif num_feature == 4:
        fig , profit_maximization = eco.prefect_competitive_market(data=data ,price=market_price,  header=Default_Header)
        st.pyplot(fig)
        st.info("profit maximization")
        st.markdown("""
        
        when the market price is equal to = `{}`
        The firm maximizes profit at the level of output `{}` ,
        where marginal revenue equals marginal cost (MR=MC=Marketing price)
        
        """.format(profit_maximization[0] , profit_maximization[1]))
    elif num_feature == 5:
        fig , profit_maximization = eco.monpoly(data=data , header=Default_Header)
        st.pyplot(fig)
        st.info('How does a monopoly choose price and output ?')
        st.markdown('• profit maximizing output is, where MR=MC')
        st.markdown('• The firm will produce the level of output, where MR=MC. = `{}` units'.format(profit_maximization[1]))

        st.warning("""The monopoly firm makes economic profit in the short run and long
run because the entry of new firms to the market is blocked.
""")
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
        if st.checkbox("Show example data", False , key='Show example data' + str(num_feature)):
            st.dataframe(data)
        fig , consumer_equilibrium , consumer_surplus = eco.marginal_utility(price=price)
        st.markdown("consumer equilibrium = `{}` when price = `{}`".format(consumer_equilibrium , price))
        st.markdown("consumer surplus = `{}` when price = `{}`".format(consumer_surplus , price))
        st.pyplot(fig)
    elif num_feature==2:#'Relation between output and labor in short run (holding other inputs fixed (capital and technology
        st.text("""Example: This table shows the relation between labor and total output,
                holding other inputs fixed (capital and technology).""")
        data =  {'Number of workers':list(range(1,8,1)) ,"Total Product": [10,30,60,80,90,90,80]}
        data = pd.DataFrame(data)
        if st.checkbox("Show example data", False , key='Show example data' + str(num_feature)):
            st.dataframe(data)
        st.pyplot(eco.relation_between_output_and_labor())

    elif num_feature ==3:
        st.text("""This table shows the relation between number of workers, output and total cost. Could
                you estimate marginal and average costs?""")
        st.pyplot(eco.average_cost_and_marginal_cost())

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
            'Relation between output and labor in short run (holding other inputs fixed (capital and technology))',
            'Marginal and Average Costs in the short run',
            'Perfectly competitive markets',
            'Monopoly'
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

if features[2] in selected_features:
    header(2)
    sidebar(2 , {"Number of workers":"Number of workers", "Total Product":"Total Product"})
    st.info("Relation between total and marginal products")
    st.markdown("""
    ```
    • When total product increases, the marginal product is positive.
    • When total product is constant (at the maximum point), the marginal
    product is zero.
    • When total product decreases, the marginal product is negative.
    ```
    """)
    st.info("Relation between average and marginal products")
    st.markdown("""
```
    • When average product increases, the marginal product is above the average
    product.
    • When average product is constant (at the maximum point), the marginal
    product equals the average product.
    • When average product decreases, the marginal product is below the average
    product.
```    """)
    st.info("Law of diminishing returns")
    st.markdown("""
    ```
    The marginal product of labor declines as the amount of labor
    increases, holding other inputs constant.
    ```
    """)

if features[3] in selected_features:
    header(3)
    sidebar(3 , {
        'Number of workers':'Number of workers',
        'output':'output',
        'Total cost':'Total cost'
    })
    st.info("The relation between average cost and marginal cost in the short run")
    st.markdown("""
    ```
        When the average cost falls, the marginal cost is below the average cost.
        When the average cost increases, the marginal cost is above the average cost.
        Marginal cost intersects average cost, when average cost is at the minimum point.

    ```
    """)
    st.info("Marginal and average costs are U-shaped")
    st.markdown("""
    ```
    The average cost curve has a U-shape and the marginal cost curve has a Ushape
    ```
    """)
    st.info("the marginal cost and the marginal product of labor")
    st.markdown("""
    ```
    • When the marginal product of labor is rising, the marginal cost of production
    is falling

    • When the marginal product of labor is falling, the marginal cost of production
    is rising.

    ```
    """)

if features[4] in selected_features:
    header(4)
    market_price = st.number_input('Market price' , 0.0)
    sidebar(4 , {'Q':'Q','MC':'MC' , 'AVC' : 'AVC' ,"ATC":"ATC"})
    st.info("Shut down in the short run")
    st.markdown("""
    ```
    The shutdown point : is the minimum point on the average variable cost.
     If the price falls below this point, the firm will shut down production
    ```
    """)

if features[5] in selected_features:
    header(5)
    set_price = st.number_input('set price' , 0.0)
    sidebar(5 , {'Q':'Q', 'P':'P'	, 'MR':'MR'	,'MC':'MC' , 'ATC':'ATC'})
    # st.info('How does a monopoly choose price and output ?')