# PyBrainage

## PyBrainage development

Here we introduce PyBrainage (beta version) which is a Brain-age model designed to estimate age (brain-age) based on structural T1-weighted MRI brain scans. Below, you will find additional information about the model and instructions on running it with your preprocessed T1-weighted MRI data using FreeSurfer.

BETA version: Your feedback/results using our model are most welcome. Please do get in touch.

### Dataset
 
The dataset used for training the model consisted of a sample size of N=58,836, covering a wide age range from 2 to 100 years. The sample included 51.1% female participants, with an average age of 46.9 years and a standard deviation of 24.4 years. The data was obtained from a healthy participant population across 82 different sites. For more in-depth information about the characteristics of this sample, please refer to the Rutherford et al 2022 study: [(https://elifesciences.org/articles/72904)] (Supplementary File 1 contains the complete sample description). Before running the model on your data, it may be worth checking if your sample overlaps with the training set as this is an important consideration when interpreting the results.


### Model inputs and model training

The model utilised neuroimaging features including cortical thickness and subcortical volumes based on the Destrieux atlas parcellations. These were extracted using FreeSurfer's aparcstats2table function with aparc.a2009s for both the left and right hemispheres and asegstats2table function to extract subcortical volumes, resulting in a total of 187 input features. The dataset was then divided into training and test sets using the train_test_split function from sklearn, with a test size of 0.2. Both training and test sets were standardized using the StandardScaler function.

An Extra Trees regression was used to predict chronological age from the neuroimaging input features in the training set. This was achieved using the ExtraTreesRegressor function from sklearn.


### Model testing and performance measure

After training, the model was evaluated using the testing set, which allowed us to assess its performance. The evaluation produced several performance measures, including a Mean Absolute Error (MAE) = 4.7 years, R-squared = .42 and a correlation coefficient, r = .66. 
 
![Alt Text](https://github.com/biondof/PyBrainage/blob/main/pybrainage.png)


## How to use PyBrainage

To extract brain-age estimates of your structural T1s using PyBrainage, you will need to follow these steps:

**1 Prepare the data**

a. Extract the neuroimaging input features based on the Destrieux brain atlas, using Freesurfer (aparcstats2table with aparc.a2009s and asegstats2table). 

b. Create a .csv file that contains 189 columns, with the first column being 'ID', the second column 'Age', and the remaining 187 neuroimaging features extracted from the previous step. The precise list of features can be found in ROIS_input_template.txt on this GitHub page.  Please ensure that the order of the columns is a perfect match to this template. Rename this file as "ROIs.csv".

c. It is advisable to run QC of your neuroimaging data before and after Freesurfer preprocessing (see https://elifesciences.org/articles/72904 for suggestions).



**2 Install PyBrainage**

It is advisable (but not necessary) to first create and activate a new Anaconda environment before installation of Pybrainage. This can be done as follows:

```python
conda create  --name pybrainage_env python=3.7 
conda activate pybrainage_env 
```

Install PyBrainage using this command:
```python
pip install py-brainage
```


**3 Run PyBrainage**
After installation, run this Python code which reads your ROIs.csv file as input to the PyBrainage model

```python
from py_brainage.trees import ExtraTreesModel   
import pandas as pd  
 
ROIs = pd.read_csv('ROIs.csv')  
model = ExtraTreesModel()  
predictions = model.predict(ROIs)  
```

You can inspect the code used to run the model in the "predict.py" file available on this git page.

**4 Check your PyBrainage output**

Successful running of the model will generate a file named "ROIs_predicted.csv" containing the original columns from "ROIs.csv" plus 1 new appended column containing the Brain-age values.


## Beyond PyBrainage: statistical analyses using brain-age estimates
Typical Brain-age analyses involve calculating Brain-PAD (Brain Predicted Age Difference), also referred to as BrainGAP, BrainAge Delta, or similar variations. Brain-PAD is determined by subtracting the chronological age from brain-age ("Age" minus "brain-age" columns, in the PyBrainage output .csv file). This metric can be utilised to examine associations with health outcomes. For further detailed discussion, refer to the work of Cole and Franke (2017). For example, larger Brain-PADs (older-appearing brains) have been associated to an increased risk in a future diagnosis of dementia in memory clinic patients (Biondo et al, 2022).

Statistical analyses involving Brain-PAD (or Brain-age) values require minimising the regression-to-the-mean effect by including linear and non-linear terms of age as covariates (see de Lange and Cole, 2020). 

## Acknowledgements and References
This software was co-created: by Andre Marquand<sup>1</sup>, Saige Rutherford<sup>1</sup>, Ayodeji Ijishakin<sup>2</sup>, Francesca Biondo<sup>2</sup> & James Cole<sup>2</sup>.
<sup>1</sup> The Donders Institute, Netherlands; <sup>2</sup> University College London (UCL), United Kingdom.


**Citations:** 

We have not used this software in published work yet. However, if you need a reference for this software, feel free to cite this page or the Rutherford et al paper in the list of references below.


**References**

Rutherford, Fraza, Dinga, Kia, Wolfers, Zabihi... Beckmann and Marquand (2022). Charting brain growth and aging at high spatial precision. eLife. [DOI](https://doi.org/10.7554/eLife.72904)

Cole and Franke (2017). Predicting age using neuroimaging: innovative brain ageing biomarkers. Trends in Neurosciences. [DOI](https://doi.org/10.1016/j.tins.2017.10.001)

Biondo, Jewell, Pritchard, Aarsland, Steves, Mueller and Cole (2022). Brain-age is associated with progression to dementia in memory clinic patients. Neuroimage: Clinical. [DOI](https://doi.org/10.1016/j.nicl.2022.103175)

de Lange & Cole (2020). Commentary: Correction procedures in brain-age prediction. Neuroimage: Clinical [DOI](https://doi.org/10.1016/j.nicl.2020.102229)






# PyBrainAge
