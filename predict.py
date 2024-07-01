import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import pickle

# Function to request file path from the user
def get_file_path(prompt):
    path = input(prompt)
    while not os.path.isfile(path):
        print("Invalid path. Please enter a valid path.")
        path = input(prompt)
    return path

# Request file paths from the user
data_vol_path = get_file_path("Enter the path for the 'aseg_stats.txt' file: ")
data_lh_path = get_file_path("Enter the path for the 'lh2009.aparc.thickness.txt' file: ")
data_rh_path = get_file_path("Enter the path for the 'rh2009.aparc.thickness.txt' file: ")
roi_template_path = get_file_path("Enter the path for the 'ROIS_input_template.txt' file: ")
age_data_path = get_file_path("Enter the path for the 'Your_database.xlsx' file: ")
model_path = get_file_path("Enter the path for the 'ExtraTreesModel' file: ")
scaler_path = get_file_path("Enter the path for the 'scaler.pkl' file: ")

# Load data
data_vol = pd.read_csv(data_vol_path, sep="\t")
data_lh = pd.read_csv(data_lh_path, sep="\t")
data_rh = pd.read_csv(data_rh_path, sep="\t")

# Reset index
data_vol.reset_index(drop=True, inplace=True)
data_lh.reset_index(drop=True, inplace=True)
data_rh.reset_index(drop=True, inplace=True)

# Concatenate data
data_features = pd.concat([data_vol, data_lh, data_rh], axis=1)

# Replace column names
data_features.columns = data_features.columns.str.replace('_and_', '&')
data_features.columns = data_features.columns.str.replace('Left-Thalamus', 'Left-Thalamus-Proper')
data_features.columns = data_features.columns.str.replace('Right-Thalamus', 'Right-Thalamus-Proper')

# Read and process ROIs input template
with open(roi_template_path, 'r') as file:
    data_rois = file.read().replace("\n", "\t")

with open(roi_template_path, 'w') as writer:
    writer.write(data_rois)

data_rois = pd.read_csv(roi_template_path, sep="\t")
data_total = pd.DataFrame(index=range(data_features.shape[0]), columns=data_rois.columns.tolist())

# Populate data_total
for i in range(0, len(data_rois.columns.tolist())):
    if i > 1:
        title = data_rois.columns.tolist()[i]
        data_total[title] = data_features.filter(like=title, axis=1).iloc[:, 0]

data_total['ID'] = data_features.filter(like='idx', axis=1).iloc[:, 0]

# Load age data
age = pd.read_excel(age_data_path)

# Map ages to data_total
array_ages = []
for index, row in data_total.iterrows():
    subject = row['ID']
    selected_line = age[age['sub'] == str(subject[32:][:-8])]
    selected_age = selected_line['age'].values[0] if not selected_line.empty else np.nan
    array_ages.append(selected_age)

data_total['Age'] = array_ages
data_total = data_total.dropna()

# Load model and scaler
model = pickle.load(open(model_path, 'rb'))
sc_X = pickle.load(open(scaler_path, 'rb'))

# Prepare data for prediction
df = data_total
IDs = df.iloc[:, 0]
Ages = df.iloc[:, 1]
data = df.iloc[:, 2:]

# Validate data
if data.isnull().values.any():
    raise ValueError('There is missing data in the dataframe')

if data.isin([np.inf, -np.inf]).values.sum() != 0:
    raise ValueError('There is an infinite value in your dataframe')

for index, row in enumerate(data.iterrows()):
    if any(isinstance(val, str) for val in row[1].values):
        raise ValueError('There is non-numeric data in the dataframe')

# Rename columns if needed
def rename_cols_to_roi_format(data):
    new_columns = []
    for col in data.columns:
        col = col.replace('_and_', '&')
        col = col.replace('Left-Thalamus', 'Left-Thalamus-Proper')
        col = col.replace('Right-Thalamus', 'Right-Thalamus-Proper')
        new_columns.append(col)
    data.columns = new_columns
    return data

# Apply scaler
try:
    data = sc_X.transform(data)
except ValueError as e:
    print("Scaler failed potentially due to feature name mismatch, attempting to rename columns and attempt scaler again.")
    data = rename_cols_to_roi_format(data)
    try:
        data = sc_X.transform(data)
        print('Scaler transformation appears successful')
    except ValueError:
        raise ValueError('Failing to apply scaler to the data. Check if the scaler is loaded correctly and/or if the data is in the correct format.') from e

# Predict
outputs = []
try:
    outputs = model.predict(data)
except:
    print("Applying the model to the data at once failed. Moving to apply the model row-by-row (slower).")
    for row in range(len(data)):
        try:
            outputs.append(model.predict(data[row].reshape(1, -1)))
        except:
            raise ValueError(f'Failed at row {row}')
print(f"Processed all {len(data)} rows successfully. Moving to save the results.")

# Save results
stacked = np.column_stack((IDs, Ages, outputs))
df2 = pd.DataFrame(stacked, columns=['ID', 'Age', 'BrainAge'])

# Calculate Brain-PAD
df2['BrainPAD'] = df2['BrainAge'] - df2['Age']

# Save output
output_path = input("Enter the path to save the 'PyBrainAge_Output.csv' file: ")
df2.to_csv(output_path, index=False)

# Plot results
df2.plot(kind='scatter', x='Age', y='BrainAge')
plt.plot([0, 100], [0, 100], color='g', label='cos')
plt.xlim(30, 100)
plt.ylim(30, 100)
plt.show()
