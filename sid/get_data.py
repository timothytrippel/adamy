import numpy as np
import pandas as pd
from sklearn.preprocessing import scale

__all__=['get_data']

def get_data(dataName):
    '''
    Input:
    name of the dataset you want to import

    Output:
    returns a training matrix 'X' and the prediction vector 'y'
    where, y: EV/EBITDA
           X: rest of the matrix

    Usage:
    X, y = get_data('consumerDiscretionary')
    '''

    # read excel files as data-frames:
    if dataName == 'consumerDiscretionary':
        consumerDiscrete = pd.read_excel('../data/U of M Student Data - Consumer Discretionary .xlsx',\
                                         'Screening', skiprows=7, na_values=['-', 'NM'] )
        dataset = consumerDiscrete.iloc[:, 5::]
    elif dataName == 'consumerStaples':
        consumerStaples  = pd.read_excel('../data/U of M Student Data - Consumer Staples.xlsx',\
                                         'Screening', skiprows=7, na_values=['-', 'NM'] )
        dataset = consumerStaples.iloc[:, 5::]
    elif dataName == 'industrials':
        industrials = pd.read_excel('../data/U of M Student Data - Industrials.xlsx',\
                                         'Screening', skiprows=7, na_values=['-', 'NM'] )
        dataset = industrials.iloc[:, 5::]
    else:
        raise ValueError('incorrect function input to get_data() ...')

    # calculate column means:
    colMean = np.nanmean(dataset, axis=0)
    
    # find indices where you need to replace:
    inds = np.where( np.isnan( dataset ) )

    # convert data-frame to numpy array:
    data = pd.DataFrame.as_matrix( dataset )

    # replace NA values with col means:
    data[inds] = np.take(colMean, inds[1])

    # clear variable value:
    dataset = None

    # replace variable with new value:
    dataset = scale(data)

    # prediction vector (EV/EBITDA):
    y = np.diviide( dataset[0], dataset[2] )

    # training matrix:
    X = np.delete( dataset, [0, 2], 1 )

    return X, y
        
