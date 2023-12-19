# Load libraries
import os
import pandas as pd
import numpy as np 
import pickle 


#load the model 
model = pickle.load(open('ExtraTreesModel', 'rb'))

#load the scaler
sc_X = pickle.load(open('scaler.pkl', 'rb'))

#read in the data
df = pd.read_csv('ROIs.csv')   

#get the subject IDs 
IDs = df.iloc[:, 0] 
Ages = df.iloc[:, 1]

#remove the subject ID and age column 
data = df.iloc[:, 2:]   

# check for missing data
if data.isnull().values.any() == True:
    raise ValueError('There is missing data in the dataframe')
inf =  data.isin([np.inf, -np.inf])

# check for infinite values in data
if inf.values.sum() != 0: 
    raise ValueError('There is an infinite value in your dataframe') 

# check for non-numeric data
for index, row in enumerate(data.iterrows()):
    if any(isinstance(val, str) for val in row[1].values):
        raise ValueError('There is non-numeric data in the dataframe') 
    

# For the scaler to work (next step), the features names in 'data' need to match the ROI_input_template.txt format. 
# However, some of the col names may be have been partially transformed to match the format used in Freesurfer. 
# This function allows those changes to be reverted back to ROI_input_template.txt format.
def rename_cols_to_roi_format(data):

    new_columns = []
    for col in data.columns:
        col = col.replace('_and_', '&')  # Replace '_and_' with '&'
        col = col.replace('Left-Thalamus', 'Left-Thalamus-Proper')  # Replace 
        col = col.replace('Right-Thalamus', 'Right-Thalamus-Proper')  # Replace 
        new_columns.append(col)

    # Assign the modified column names 
    data.columns = new_columns
    return data



#apply the scaler transformation to the data 
try:
    data = sc_X.transform(data)
except ValueError as e:
    print("Scaler failed potentially due to feature name mismatch, attempting to rename columns and attempt scaler again.")
    data = rename_cols_to_roi_format(data)  # attempt renaming function
    try:
        data = sc_X.transform(data) #attempt scaler again
        print('Scaler transformation appears successful')
    except ValueError:
        raise ValueError('Failing to apply scaler to the data. Check if the scaler is loaded correctly and/or if the data is in the correct format.') from e


# predict
outputs = []

try:
    # predict Brain-age (apply ExtraTrees model to whole array at once)
    outputs = model.predict(data)
    
except:
    print(f"Applying the model to the data at once failed. Moving to apply the model row-by-row (slower).")
    # predict Brain-age row-by-row
    for row in range(len(data)):
        try:
            outputs.append(model.predict(data[row].reshape(1, -1))) 
        except:
            raise ValueError(f'Failed at row {row}')
print(f"Processed all {len(data)} rows successfully. Moving to save the results.")


stacked = np.column_stack((IDs, Ages, outputs))

# Convert to a pandas dataframe and add column name
df2 = pd.DataFrame(stacked, columns=['ID', 'Age','BrainAge'])

# Calculate Brain-PAD (Predicted Age Difference)
df2['BrainPAD']=df2['BrainAge']-df2['Age']

#save the output
df2.to_csv('PyBrainAge_Output.csv') #modify output filename/path as needed 
