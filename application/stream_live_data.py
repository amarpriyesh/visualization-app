from grequests import AsyncRequest
import requests
import pandas as pd
import json
from pandas import json_normalize






def get_user_data(api):
        response = requests.get(f"{api}")
        
        if response.status_code == 200:
            data = json.dumps(response.json())
            print("sucessfully fetched the data with parameters provided")
            dict = json.loads(data)
            df2 = json_normalize(dict['people']) 
            return(df2)
            
        else:
            print(
                f"Hello person, there's a {response.status_code} error with your request")
            

url="http://api.open-notify.org/astros.json"
df1 = pd.DataFrame()
df_union= pd.concat([df1, get_user_data(url)]).drop_duplicates(keep='first')
