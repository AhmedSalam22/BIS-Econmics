import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point
import streamlit as st


def point_of_intersection(A,B,C,D):
    """
    # Given these endpoints
    #line 1
    A = (X, Y)
    B = (X, Y)

    #line 2
    C = (X, Y)
    D = (X, Y)

    # Compute this:
    point_of_intersection = (X, Y)
    
    resources:
    https://stackoverflow.com/a/56791549
    """
    line1 = LineString([A, B])
    line2 = LineString([C, D])

    int_pt = line1.intersection(line2)
    point_of_intersection = int_pt.x, int_pt.y

    return point_of_intersection


class Economics():
    def demand_supply_cruve(self ,
                             data=None ,
                             shift_demand_curve = 0.0 ,
                             shift_supply_curve = 0.0 ,
                             header={'price':'price' , 'Demand':'Demand' , 'Supply':'Supply'}):
        """Graph demand and supply curve
        inputs
        --------------------------------
        Data is a {price:[] , 'Demand':[1,2,3....] , 'Supply':[1,2,3,....] } per unit or Use DataFrame

        """
        try:
            if  data == None:
                data =  {'price':list(range(0,201,10)) ,'Demand':list(range(0,401,20))[::-1] , 'Supply':list(range(0,401,20))}
                data = pd.DataFrame(data)
        except ValueError:
            pass
      
        demand_supply_intersection = point_of_intersection(A=(data[header['Demand']].iloc[0] ,data[header['price']].iloc[0]) ,
                                B=(data[header['Demand']].iloc[-1] ,data[header['price']].iloc[-1]), 
                                C=(data[header['Supply']].iloc[-1] ,data[header['price']].iloc[-1]),
                                D= (data[header['Supply']].iloc[0] ,data[header['price']].iloc[0]),
                                 )

        fig, ax = plt.subplots()
        sns.lineplot( x=data[header['Demand']], y=data[header["price"]]  , label="Demand")
        sns.lineplot( data=data, x=header['Supply'], y=header['price'] , label="Supply")
        
        if shift_demand_curve != 0.0:
            data['shift_demand'] = data[header['Demand']] * (1 + shift_demand_curve)
            sns.lineplot( x=data['shift_demand'], y=data[header["price"]]  , label="shifted_Demand" )

        if shift_supply_curve != 0.0:
            data['shift_supply'] = data[header['Supply']] * (1 + shift_demand_curve)
            sns.lineplot( x=data['shift_supply'], y=data[header["price"]]  , label="shifted_Supply")
        # change style for shifted_Supply and shifted_Demand line to --- dashed line
        for ax_i in ax.lines[2:]:
            ax_i.set_linestyle("--")


        ax.set_xlabel('Quantity')
        ax.set_ylabel('price')
        # add Market equilibrium maket to the graph
        ax.annotate('Market equilibrium {}'.format(demand_supply_intersection),
            xy=demand_supply_intersection, xycoords='data',
            xytext=(0.8, 0.95), textcoords='axes fraction',
            arrowprops=dict(facecolor='red', shrink=0.05),
            horizontalalignment='right', verticalalignment='top')

        return fig


    def marginal_utility(self  , data=None , price=0, header={'quantity':'quantity' , 'Total utility':'Total utility'}):
        """Marginal utility: is the change in total utility from consuming an additional unit of good. """
        try:
            if  data == None:
                data =  {'quantity':list(range(1,7)) ,'Total utility':[20,36,46,52,54,52]}
                data = pd.DataFrame(data)
        except ValueError:
            pass
        
        data['Marginal utility'] = data[header['Total utility']].diff()
        data['Marginal utility'].iloc[0] = data[header['Total utility']].iloc[0].copy()

        consumer_equilibrium = data[data['Marginal utility'] >= price][header['quantity']].max()
        Consumer_surplus = (data[data['Marginal utility'] >= price]['Marginal utility'] -price).sum()

        print("consumer_equilibrium" , consumer_equilibrium ,"Consumer_surplus" , Consumer_surplus)

        fig, ax = plt.subplots()
        # marginal utility
        sns.barplot(data=data.sort_values('Marginal utility' , ascending=False) , x=header['quantity'],y='Marginal utility' , color="blue" , label="Marginal utility")
        #Demand Curve
        # sns.lineplot(data=data , x='quantity' ,y='Marginal utility', color='green', label='estimated Demand Curve(marginal utility curve)')
        # price line to determine consumer surplus and consumer equilibrium
        if price != 0:
            plt.axhline(y=price, color='r', linestyle='-' , label="Price")
        plt.legend()
        return fig , consumer_equilibrium , Consumer_surplus

    def relation_between_output_and_labor(self , data=None ,
                                                header={"Number of workers":"Number of workers",
                                                        "Total Product":"Total Product"
                                                        }):


        try:
            if  data == None:
                data =  {'Number of workers':list(range(1,8,1)) ,"Total Product": [10,30,60,80,90,90,80]}
                data = pd.DataFrame(data)
        except ValueError:
            pass
        
        data['Marginal product'] = data[header['Total Product']].diff()
        data['Marginal product'].iloc[0] = data[header['Total Product']].iloc[0].copy()
        
        data["Average Product"] = data[header["Total Product"]] / data[header["Number of workers"]]


        fig, ax = plt.subplots()
        sns.lineplot(data=data , x=header['Number of workers'] , y=header['Total Product'] , label='Total Product')
        sns.lineplot(data=data , x=header['Number of workers'] , y='Marginal product' , label='Marginal product')
        sns.lineplot(data=data , x=header['Number of workers'] , y='Average Product', label='Average Product')

        return fig

    
    def average_cost_and_marginal_cost(self , data=None , streamlit=True,  header={
        'Number of workers':'Number of workers',
        'output':'output',
        'Total cost':'Total cost'
    }):
        try:
            if  data == None:
                data =  {'Number of workers':list(range(0,7,1)) ,
                         'output':[0,200,450,550,600,625, 640] ,
                         'Total cost':[800,1400,2000,2600,3200,3800,4400]
                        }
                data = pd.DataFrame(data)
        except ValueError:
            pass
        
        data['Marginal Cost'] = data[header['Total cost']].diff() / data[header['output']].diff() 
        data['Marginal Cost'] =data['Marginal Cost'].fillna(0 )

        data['Average Cost'] = data[header['Total cost']] / data[header['output']]
        data['Average Cost'] =data['Average Cost'].fillna(0 )

        if streamlit == True:
            st.dataframe(data)

        fig, ax = plt.subplots()
        sns.lineplot(data=data , x=header['Number of workers'] , y='Marginal Cost' , label='Marginal Cost')
        sns.lineplot(data=data , x=header['Number of workers'] , y='Average Cost' , label='Average Cost')
        ax.set_ylabel('Cost')

        return fig


    def prefect_competitive_market(self , data , price=0 , header={'Q':'Q','MC':'MC' , 'AVC' : 'AVC' ,"ATC":"ATC"}):
        
        data['Price'] = price
        profit_maximization = point_of_intersection(A=(data[header['MC']].iloc[0] ,data[header['Q']].iloc[0]) ,
                        B=(data[header['MC']].iloc[-1] ,data[header['Q']].iloc[-1]), 
                        C=(data['Price'].iloc[-1] ,data[header['Q']].iloc[-1]),
                        D= (data['Price'].iloc[0] ,data[header['Q']].iloc[0]),
                            )
        # profit_maximization =  data[data[header['MC']] <= price][header['MC']].max()
        # print(profit_maximization)
        fig, ax = plt.subplots()
        sns.lineplot(data=data , x=header['Q'] , y=header['MC'] , label='MC')
        sns.lineplot(data=data , x=header['Q'] , y=header['AVC'] , label='AVC')
        sns.lineplot(data=data , x=header['Q'] , y=header['ATC'] , label='ATC')

        shutdown_point =    data[data[header['AVC']] == data[header['AVC']].min()][header['Q']].values[0] , data[header['AVC']].min() 
        if price != 0:
            sns.lineplot(data=data , x=header['Q'] , y='Price' , label="Market Price")

        ax.annotate('shutdown point {}'.format(shutdown_point),
            xy=shutdown_point, xycoords='data',
            xytext=(0.8, 0.50), textcoords='axes fraction',
            arrowprops=dict(facecolor='red', shrink=0.01),
            horizontalalignment='right', verticalalignment='top')

     
        return fig , profit_maximization


    def monpoly(self , data , header={'Q':'Q', 'P':'P'	, 'MR':'MR'	,'MC':'MC' , 'ATC':'ATC'}):

        profit_maximization = point_of_intersection(A=(data[header['MC']].iloc[0] ,data[header['Q']].iloc[0]) ,
                        B=(data[header['MC']].iloc[-1] ,data[header['Q']].iloc[-1]), 
                        C=(data['MR'].iloc[-1] ,data[header['Q']].iloc[-1]),
                        D= (data['MR'].iloc[0] ,data[header['Q']].iloc[0]),
                            )
        print("profit_maximization", profit_maximization)

        fig , ax = plt.subplots()
        sns.lineplot(data=data , x=header['Q'] , y=header['MC'] , label='MC')
        sns.lineplot(data=data , x=header['Q'] , y=header['MR'] , label='MR')
        sns.lineplot(data=data , x=header['Q'] , y=header['ATC'] , label='ATC')

        ax.set_ylabel('Price')
        ax.set_xlabel('Quantity')

        ax.annotate('profit maximization {}'.format((profit_maximization[1],profit_maximization[0])),
                    xy=(profit_maximization[1],profit_maximization[0]), xycoords='data',
                    xytext=(0.8, 0.95), textcoords='axes fraction',
                    arrowprops=dict(facecolor='red', shrink=0.05),
                    horizontalalignment='right', verticalalignment='top')

        return fig , profit_maximization

