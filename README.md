# PyBrainAge

## PyBrainAge development
Here we introduce PyBrainAge (beta version) which is a Brain-age model designed to estimate age (brain-age) based on structural T1-weighted MRI brain scans. Below, you will find additional information about the model and instructions on running it with your preprocessed T1-weighted MRI data using FreeSurfer.
BETA version: Your feedback/results using our model are most welcome. Please do get in touch.

### Dataset
 Data used for training the model consisted of a sample size of N=58,836 from the UK Biobank dataset, covering a wide age range from 2 to 100 years. The sample included 51.1% female participants, with an average age of 46.9 years and a standard deviation of 24.4 years. The data was obtained from a healthy participant population across 82 different sites. For more in-depth information about the characteristics of this sample, please refer to the Rutherford et al 2022 study: [(https://elifesciences.org/articles/72904)] (Supplementary File 1 contains the complete sample description). Before running the model on your data, it may be worth checking if your sample overlaps with the training set as this is an important consideration when interpreting the results.

**Warning**: Do not use the PyBrainAge model if your input data includes UK Biobank data given this was used to train the model. Including UK Biobank data would comprimise the validity of your results.

### Model inputs and model training
The model utilised neuroimaging features including cortical thickness and subcortical volumes based on the Destrieux atlas parcellations. These were extracted using FreeSurfer's aparcstats2table function with aparc.a2009s for both the left and right hemispheres and asegstats2table function to extract subcortical volumes, resulting in a total of 187 input features. The dataset was then divided into training and test sets using the train_test_split function from sklearn, with a test size of 0.2. Both training and test sets were standardized using the StandardScaler function.

An Extra Trees regression was used to predict chronological age from the neuroimaging input features in the training set. This was achieved using the ExtraTreesRegressor function from sklearn.


### Model testing and performance measure
After training, the model was evaluated using the testing set, which allowed us to assess its performance. The evaluation produced several performance measures, including a Mean Absolute Error (MAE) = 4.7 years, R-squared = .42 and a correlation coefficient, r = .66. 
 
![Alt Text](https://github.com/james-cole/PyBrainage/blob/main/pybrainage.png)


## How to use PyBrainAge
To extract brain-age estimates of your structural T1s using PyBrainAge, you will need to follow these steps:

**1 Prepare the data**

a. Extract the neuroimaging input features based on the Destrieux brain atlas, using Freesurfer (aparcstats2table with aparc.a2009s and asegstats2table). 

b. Create a .csv file that contains 189 columns, with the first column being 'ID', the second column 'Age', and the remaining 187 neuroimaging features extracted from the previous step. The precise list of features can be found in ROIS_input_template.txt on this GitHub page. Please ensure that the order and naming of the columns is a perfect match to this template. Let's refer to this file as "ROIs.csv".

c. It is advisable to run QC of your neuroimaging data before and after Freesurfer preprocessing (see https://elifesciences.org/articles/72904 for suggestions).

**Warning**: Do not use the PyBrainAge model if your input data includes UK Biobank data given this was used to train the model. Including UK Biobank data would comprimise the validity of your results.

**2 Create a Conda Environment**

Create and activate a new Anaconda environment as follows:

```python
conda create  --name pybrainage_env python=3.7 scikit-learn=0.24.2 pandas=1.3.4 numpy=1.20.3
conda activate pybrainage_env 
```

Here we are specifying precise versions of Python, scikit-learn, pandas, and numpy to operate within the isolated environment, ensuring it does not interfere with your other environments. This approach is essential to eliminate warning messages and potential errors caused by version conflicts, especially concerning scikit-learn.

However, please be aware that even with these configurations, you may encounter the following message. Please ignore!

```python
UserWarning: Trying to unpickle estimator StandardScaler from version 1.2.0 when using version 0.24.2. This might lead to breaking code or invalid results. Use at your own risk 
```

To verify whether the activation of the "pybrainage_env" environment was successful, execute the following command:

```
conda env list
```
You should observe an asterisk (*) next to "pybrainage_env," confirming that you are currently working within the "pybrainage_env" environment you have just created.

**3 Run PyBrainAge using predict.py**
You can now proceed to run predict.py (found on this github page).
The inputs required to this script are: 1) your ROIs.csv input file, 2) scaler.pkl (found on this github page) 3) ExtraTreesModel (downloaded via [Zenodo](https://zenodo.org/), using this link )
The output is a PyBrainAge_Output.csv file containing ID, Age, Brain-Age and Brain-PAD (see note below) 


## Brain-PAD
Typical Brain-age analyses involve calculating Brain-PAD (Brain Predicted Age Difference), also referred to as BrainGAP, BrainAge Delta, or similar variations. Brain-PAD is determined by subtracting chronological age from Brain-age ("Age" minus "Brain-age" columns, which is already calculated for you in the PyBrainAge_Output.csv file). This metric can be utilised to examine associations with health outcomes. For further detailed discussion, refer to the work of Cole and Franke (2017). For example, larger Brain-PADs (older-appearing brains) have been associated to an increased risk in a future diagnosis of dementia in memory clinic patients (Biondo et al, 2022).

Statistical analyses involving Brain-PAD (or Brain-age) values require minimising the regression-to-the-mean effect by including linear and non-linear terms of age as covariates (see de Lange and Cole, 2020). 

## Acknowledgements and References
This software was co-created: by Andre Marquand<sup>1</sup>, Saige Rutherford<sup>1</sup>, Ayodeji Ijishakin<sup>2</sup>, Francesca Biondo<sup>2</sup> & James Cole<sup>2</sup>.
<sup>1</sup> The Donders Institute, Netherlands; <sup>2</sup> University College London (UCL), United Kingdom.

### Citations: 
We have not used this software in published work yet. However, if you need a reference for this software, feel free to cite this page or the Rutherford et al paper in the list of references below.

### References
Rutherford, Fraza, Dinga, Kia, Wolfers, Zabihi... Beckmann and Marquand (2022). Charting brain growth and aging at high spatial precision. eLife. [DOI](https://doi.org/10.7554/eLife.72904)

Cole and Franke (2017). Predicting age using neuroimaging: innovative brain ageing biomarkers. Trends in Neurosciences. [DOI](https://doi.org/10.1016/j.tins.2017.10.001)

Biondo, Jewell, Pritchard, Aarsland, Steves, Mueller and Cole (2022). Brain-age is associated with progression to dementia in memory clinic patients. Neuroimage: Clinical. [DOI](https://doi.org/10.1016/j.nicl.2022.103175)

de Lange & Cole (2020). Commentary: Correction procedures in brain-age prediction. Neuroimage: Clinical [DOI](https://doi.org/10.1016/j.nicl.2020.102229)
