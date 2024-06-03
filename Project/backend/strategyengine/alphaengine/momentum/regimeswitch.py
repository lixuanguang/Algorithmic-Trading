# Specify project path
import sys
import os

database = os.path.join(os.getcwd(),'Project','data')
filepath = os.path.join(os.getcwd(),'Project','alphaengine','momentum')

import pandas as pd
# Retrieve data
price = pd.read_csv(os.path.join(database, 'acwi.csv'))
print(price)
