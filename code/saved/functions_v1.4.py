
import numpy as np
import math
import pandas as pd
import itertools

########################################################### FUNCTIONS


### FUNCTION FOR LOG TRANSFORMATIONS AND/OR NORMALIZATION

def log_and_normalize (data, log, norm_type):
    if log == 'log':
        data = np.log(data)
    if norm_type == 1:
        data = (data-np.mean(data))/np.std(data)  # std normalisation
    elif norm_type == 2:
        data = (data-min(data))/(max(data)-min(data))      #  min_max_min
    elif norm_type == 3:
        data = (data-np.mean(data))/(max(data)-min(data))  # mean norm

    return data



### FUNCTION FOR HOT ENCODING

def hot_encode (data, directions):
    if directions == 'yes':
        data = pd.get_dummies(data, prefix=data.name[:3], drop_first=True)
    return data

## FUNCTION TO TRANSFORM DATA using log_and_normalize AND hot_encode FUNCTIONS :

def transform_data(x0, y0):

#    ord_cat=pd.DataFrame([])
#    ord_cat=pd.DataFrame(x0['view2'].cat.codes)
#    ord_cat.columns=['view']

    nochange=['basement','grade']
    log=["sqft_living", 'sqft_lot' ]
    hot=[ 'decade', 'zipcode', 'view',  'waterfront']

    asis=x0[nochange]

    x1=pd.DataFrame([])

    # log transformations
    y1=log_and_normalize(y0, 'log', 0)

    for col in log:
        x1[col]=log_and_normalize(x0[col], 'log', 0)


    # One hot encode categoricals
    for col in hot:
        new_cols=hot_encode(x0[col], 'yes')
        x1 = pd.concat([x1, new_cols], axis=1)

#    x1 = pd.concat([x1, ord_cat, asis], axis=1)
    x1 = pd.concat([x1,  asis], axis=1)

    return x1,y1

### TO GET COEFFECIENTS FROM MODEL OBJECT

def get_coeff( decade,zipcode, grade, water,view, coef_df):

    intercept=coef_df[coef_df['Column'] == "const"]["Value"].tolist()[0]
    sqft_living_coef=coef_df[coef_df['Column'] == "sqft_living"]["Value"].tolist()[0]
    sqft_lot_coef=coef_df[coef_df['Column'] == "sqft_lot"]["Value"].tolist()[0]
    basement_coef=coef_df[coef_df['Column'] == "basement"]["Value"].tolist()[0]
    grade_coef=coef_df[coef_df['Column'] == "grade"]["Value"].tolist()[0]

    if water == 1:
        water_coef=coef_df[coef_df['Column'] == "wat_YES"]["Value"].tolist()[0]
    else:
        water_coef=0

    try:
        decade_coef=coef_df[ coef_df['Column'].str.endswith(decade)] ["Value"].tolist()[0]
    except:
        decade_coef=0

    if len(str(zipcode)) != 5:
        zipcode_coef=0
    else:
        try: zipcode_coef=coef_df[coef_df['Column'].str.endswith(str(zipcode))]["Value"].tolist()[0]
        except: zipcode_coef=0

    if view  not in ['NONE','FAIR','GOOD','EXCELLENT']:
        view_coef=0
    else:
        try: view_coef=coef_df[coef_df['Column'].str.endswith(view)]["Value"].tolist()[0]
        except: view_coef=0

    return intercept, sqft_living_coef, sqft_lot_coef, basement_coef, water_coef, grade_coef, decade_coef, zipcode_coef, view_coef


