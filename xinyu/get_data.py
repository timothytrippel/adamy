import numpy as np
import pandas as pd
from sklearn.preprocessing import scale

__all__=['load_data_frames', 'mean_fill_nan_entries', 'median_fill_nan_entries', 'get_raw_data', 'get_standardized_data']

rename_col_dict = {
	'Total Enterprise Value [My Setting] [12/31/2016] ($USDmm, Historical rate)': 't_ev',
	'Total Revenue [LTM] ($USDmm, Historical rate)':							  't_rev',
	'EBITDA [LTM] ($USDmm, Historical rate)': 									  'ebitda',
	'EBITDA Margin % [LTM]': 													  'ebitda_margin',
	'TEV/LTM Total Revenues [My Setting] [LTM as of 12/31/2016] (x)': 			  't_ev/t_rev',
	'TEV/LTM EBITDA [My Setting] [LTM as of 12/31/2016] (x)': 					  't_ev/ebitda',
	'Est. Annual Revenue Growth - 1 Yr % - Capital IQ [Latest] (%)':			  'est_ann_rev_gr_minus_1yr_minus_capiq',
	'Est. Annual EBITDA Growth - 1 Yr % - Capital IQ [Latest] (%)':				  'est_ann_ebitda_gr_minus_1yr_minus_capiq',
	'Total Revenues, 1 Yr Growth % [LTM] (%)':									  't_rev_1yr_growth',
	'EBITDA, 1 Yr Growth % [LTM] (%)':											  'ebitda_1yr_growth',
	'Total Revenues, 3 Yr CAGR % [LTM] (%)':									  't_rev_3_yr_cagr',
	'EBITDA, 3 Yr CAGR % [LTM] (%)':											  'ebitda_3yr_cagr',
	'Total Revenues, 5 Yr CAGR % [LTM] (%)':									  't_rev_5yr_cagr',
	'EBITDA, 5 Yr CAGR % [LTM] (%)':											  'ebitda_5yr_cagr',
	'Return on Assets % [LTM]':													  'return_on_assets',
	'Return on Equity % [LTM]':													  'return_on_equity',
	'Capex as % of Revenues [Latest Annual] (%)':								  'capex_as_percent_rev',
	'EBITDA / Interest Exp. [LTM]':												  'ebitda/interest_exp',
	'Total Debt/Capital % [Latest Annual]':										  't_debt/cap_percent',
	'Total Debt/Equity % [Latest Annual]':										  't_debt/equity_percent'
	}

def load_data_frames():
	# read excel files as data-frames:
	consumerDiscrete = pd.read_excel('../data/U of M Student Data - Consumer Discretionary .xlsx', 'Screening', skiprows=7, na_values=['-', 'NM'] )
	consumerStaples  = pd.read_excel('../data/U of M Student Data - Consumer Staples.xlsx', 'Screening', skiprows=7, na_values=['-', 'NM'] )
	industrials      = pd.read_excel('../data/U of M Student Data - Industrials.xlsx', 'Screening', skiprows=7, na_values=['-', 'NM'] )

	# remove string data columns
	consumerDiscrete = consumerDiscrete.iloc[:, 5::]
	consumerStaples  = consumerStaples.iloc[:, 5::]
	industrials      = industrials.iloc[:, 5::]

	# rename data columns
	consumerDiscrete.rename(columns=rename_col_dict, inplace=True)
	consumerStaples.rename(columns=rename_col_dict, inplace=True)
	industrials.rename(columns=rename_col_dict, inplace=True)

	# list of all the data sets:
	dataSet = [consumerDiscrete, consumerStaples, industrials]

	return dataSet

def mean_fill_nan_entries( data_frame, is_df=True ):
	column_means 	  		= np.nanmean( data_frame, axis=0 ) 	   # calculate column means
	indicies   			    = np.where( np.isnan( data_frame ) )   # find indices where you need to replace
	if is_df:
		data_matrix 	  	= pd.DataFrame.as_matrix( data_frame ) # convert data-frame to numpy array
	else:
		data_matrix 		= data_frame
	data_matrix[ indicies ] = np.take( column_means, indicies[1] ) # replace NA values with col means
	return data_matrix

def median_fill_nan_entries( data_frame, is_df=True ):
	column_means 	  		= np.nanmedian( data_frame, axis=0 )   # calculate column means
	indicies   			    = np.where( np.isnan( data_frame ) )   # find indices where you need to replace
	if is_df:
		data_matrix 	  	= pd.DataFrame.as_matrix( data_frame ) # convert data-frame to numpy array
	else:
		data_matrix 		= data_frame
	data_matrix[ indicies ] = np.take( column_means, indicies[1] ) # replace NA values with col means
	return data_matrix

def get_raw_data():
	data_set = load_data_frames()
	for data_frame_index in range(len( data_set )):
		data_set[data_frame_index] = median_fill_nan_entries( data_set[data_frame_index] )
	return data_set

def get_standardized_data():
	data_set = load_data_frames()
	for data_frame_index in range(len( data_set )):
		data_set[data_frame_index] = scale(mean_fill_nan_entries( data_set[data_frame_index] ))
	return data_set
