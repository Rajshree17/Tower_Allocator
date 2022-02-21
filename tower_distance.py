from math import sin, cos, sqrt, atan2, radians
import pandas as pd
import numpy as np
import os
import datetime



def distance(tower_lat1 ,tower_lon1 ,cust_lat2, cust_lon2):
    try:
        R = 6373.0   # approximate radius of earth in km

        dlon = cust_lon2 - tower_lon1
        dlat = cust_lat2 - tower_lat1

        a = sin(dlat / 2)**2 + cos(tower_lat1) * cos(cust_lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c

        return distance 
    except Exception as err:
        print(f"Error : tower_distance | distance | Details : {err}")

def  closest_tower(df_towers,df_customers):
    try:
        tem_dict = {'Towers':[],'Customers':[]}
        tem_lst = []
        for index, tower_data in df_towers.iterrows(): 
            # print(str(tower_data['Towers']) )
            lst_towers = tem_dict['Towers']
            d = tower_data['Towers']
            lst_towers.append(str(d))
            for index, cust_data in df_customers.iterrows(): 
                ds = distance(radians(tower_data['Latitude']) ,radians(tower_data['Longitude']) ,radians(cust_data['Cust_lat']) ,radians(cust_data['Cust_long']) )
                
                if ds <= 4.000:
                    tem_lst.append(cust_data['Customers'])
            

            if  tem_lst != []:
                cust_lst = tem_dict["Customers"]
                cust_lst.append(str(tem_lst))
            else :
                lst_towers.remove(str(d))
            
            tem_lst.clear() 


        df = pd.DataFrame(tem_dict)
        folder = "media/output/"
        date = datetime.datetime.now()
        today_d = date.strftime("%d_%m_%y")
        file_name = f"output_{today_d}.xlsx"
        df.to_excel(f"{folder}{file_name}")
        
        return file_name
    except Exception as err:
        print(f"Error : tower_distance | closest_tower | Details : {err}")

def get_closest_tower_data(file_path):
    try:
        towers = pd.read_excel(file_path, 'Towers')
        df_towers = towers.astype(object).replace(np.nan, '')
        df_towers['list of customer'] = ""

        customers = pd.read_excel(file_path, 'Customers')
        df_customers  = customers.astype(object).replace(np.nan, '')
        final_file = closest_tower(df_towers,df_customers)
        return final_file
    except Exception as err:
        print(f"Error : tower_distance | get_closest_tower_data | Details : {err}")



