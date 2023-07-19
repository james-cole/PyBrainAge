import os
import pandas as pd
import sklearn 
from sklearn.ensemble import ExtraTreesRegressor 
from sklearn.preprocessing import StandardScaler 
import pickle 
import numpy as np 

#load in the model 
model = pickle.load(open('../PyBrainage_model', 'rb'))

#read in the data
df = pd.read_csv('data/ROIs.csv')    

#get the subject IDs 
IDs = df.iloc[:, 0] 
Ages = df.iloc[:, 1]

#remove the subject ID and age column 
data = df.iloc[:, 2:]   
 
# check for missing data
if data.isnull().values.any() == True:
    raise ValueError('There is missing data in the dataframe')

inf =  data.isin([np.inf, -np.inf])
if inf.values.sum() != 0: 
    raise ValueError('There is an infinite value in your dataframe') 

# check for non-numeric data
for index, row in enumerate(data.iterrows()):
    if any(isinstance(val, str) for val in row[1].values):
        raise ValueError('There is non-numeric data in the dataframe') 
    
#pre_process the data 
sc_X = StandardScaler()

#pre_process the data 
try:
    data = sc_X.fit_transform(data)
except ValueError:
    raise ValueError ('Failing to normalise (StandardScaler) the data. Check the data is in the correct format')


outputs = []

try:
    # predict Brainage (apply model to whole array at once)
    outputs = model.predict(data)
    
except:
    print(f"Applying the model to the data at once failed. Moving to apply the model row-by-row (slower).")
    # predict Brainage row-by-row
    for row in range(len(data)):
        try:
            outputs.append(model.predict(data[row].reshape(1, -1))) 
        except:
            raise ValueError(f'Failed at row {row}')
print(f"Processed all {len(data)} rows successfully. Moving to save the results.")


# Stack the two arrays horizontally
stacked = np.column_stack((data, outputs))

# Convert to a pandas dataframe and add column name
df2 = pd.DataFrame(stacked, columns=list(range(data.shape[1])) + ['BrainAge'])

# Add the subject IDs back in
df2.insert(0, 'ID', IDs)
df2.insert(1, 'Age', Ages)

#save the data
df2.to_csv('data/ROIs_predicted.csv') 