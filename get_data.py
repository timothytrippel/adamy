import numpy as np
import pandas as pd
import scipy.stats as stats
from sklearn.preprocessing import scale

__all__=['get_data']

def get_data():
    '''
    Output:
    returns a list of 3 data-sets scaled to have unit norm
    '''

    # read excel files as data-frames:
    consumerDiscrete = pd.read_excel('./data/U of M Student Data - Consumer Discretionary .xlsx',\
                                     'Screening', skiprows=7, na_values=['-', 'NM'] )
    consumerStaples  = pd.read_excel('./data/U of M Student Data - Consumer Staples.xlsx',\
                                     'Screening', skiprows=7, na_values=['-', 'NM'] )
    industrials      = pd.read_excel('./data/U of M Student Data - Industrials.xlsx',\
                                     'Screening', skiprows=7, na_values=['-', 'NM'] )

    # remove string data columns
    consumerDiscrete = consumerDiscrete.iloc[:, 5::]
    consumerStaples  = consumerStaples.iloc[:, 5::]
    industrials      = industrials.iloc[:, 5::]

    # list of all the data sets:
    dataSet = [consumerDiscrete, consumerStaples, industrials]

    for i in range( len(dataSet) ):
        # calculate column means:
        colMean = stats.nanmean(dataSet[i], axis=0)

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
        
