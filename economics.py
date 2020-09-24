import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point


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