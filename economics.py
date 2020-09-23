import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point
import time
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
        sns.lineplot( x=data[header['Demand']], y=data["price"]  , label="Demand")
        sns.lineplot( data=data, x=header['Supply'], y=header['price'] , label="Supply")
        
        if shift_demand_curve != 0.0:
            data['shift_demand'] = data[header['Demand']] * (1 + shift_demand_curve)
            sns.lineplot( x=data['shift_demand'], y=data["price"]  , label="shifted_Demand" )

           

        if shift_supply_curve != 0.0:
            data['shift_supply'] = data[header['Supply']] * (1 + shift_demand_curve)
            sns.lineplot( x=data['shift_supply'], y=data["price"]  , label="shifted_Supply")

        for ax_i in ax.lines[2:]:
            ax_i.set_linestyle("--")


        ax.set_xlabel('Quantity')
        ax.set_ylabel('price')

        ax.annotate('Market equilibrium {}'.format(demand_supply_intersection),
            xy=demand_supply_intersection, xycoords='data',
            xytext=(0.8, 0.95), textcoords='axes fraction',
            arrowprops=dict(facecolor='red', shrink=0.05),
            horizontalalignment='right', verticalalignment='top')

        time.sleep(5)
        return fig

