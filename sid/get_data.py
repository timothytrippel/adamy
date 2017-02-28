import numpy as np
import pandas as pd
from sklearn.preprocessing import scale

__all__=['get_data']

def get_data(dataName):
    '''
    Output:
    returns a list of 3 data-sets scaled to have zero mean and unit variance
    '''

    # read excel files as data-frames:
    if dataName == consumerDiscretionary or dataName == allTheData :
        consumerDiscrete = pd.read_excel('../data/U of M Student Data - Consumer Discretionary .xlsx',\
                                         'Screening', skiprows=7, na_values=['-', 'NM'] )
        consumerDiscrete = consumerDiscrete.iloc[:, 5::]
    elif dataName == consumerStaples or dataName == allTheData:
        consumerStaples  = pd.read_excel('../data/U of M Student Data - Consumer Staples.xlsx',\
                                         'Screening', skiprows=7, na_values=['-', 'NM'] )
        consumerStaples  = consumerStaples.iloc[:, 5::]
    elif dataName == industrials or dataName == allTheData:
        industrials      = pd.read_excel('../data/U of M Student Data - Industrials.xlsx',\
                                         'Screening', skiprows=7, na_values=['-', 'NM'] )
        industrials      = industrials.iloc[:, 5::]
    else:
        raise ValueError('incorrect function input to get_data() ...')

    # list of all the data sets:
    if dataName == consumerDiscretionary:
        dataSet = [consumerDiscrete]
    elif dataName == consumerStaples:
        dataSet = [consumerStaples]
    elif dataName == industrials:
        dataSet = [industrials]
    elif dataName == allTheData :
        dataSet = [consumerDiscrete, consumerStaples, industrials]

    for i in range( len(dataSet) ):
        # calculate column means:
        colMean = np.nanmean(dataSet[i], axis=0)

        # find indices where you need to replace:
        inds = np.where( np.isnan( dataSet[i] ) )

        # convert data-frame to numpy array:
        data = pd.DataFrame.as_matrix( dataSet[i] )

        # replace NA values with col means:
        data[inds] = np.take(colMean, inds[1])

        # clear variable value:
        dataSet[i] = None

        # replace variable with new value:
        dataSet[i] = scale(data)

    return dataSet
        
