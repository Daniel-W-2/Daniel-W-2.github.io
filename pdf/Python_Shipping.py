# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

filename = 'shippingdata.csv'
data = pd.read_csv(filename, index_col = 0)

# Pandas initial investigation
data.head()
data.info()
data.shape
data.describe()
data.dtypes
data.columns

# simple multiple column selection
disc = data[['Warehouse_block','Discount_offered']]

# simple row selection
first5 = data[0:5]

# return a specific transcations
data_search = data.loc[[27,58],['Warehouse_block', 'Discount_offered']]
data_iloc = data.iloc[:,[1,6]]

# Changing index to support loc slicing easily 
data_ind = data.set_index('Weight_in_gms').sort_index(ascending = True)
data_2kg_3kg = data_ind.loc[ '2000':'3000' ]

data_ind_block = data.set_index('Warehouse_block').sort_index(ascending = True)
data_AC = data_ind_block = data_ind_block.loc[['A','C'],'Discount_offered']

# Simple Histogram example




# if / elif / else
x = 6

if x > 10 : 
    print('High Discount Offered ' + str(x) + ' percent')
elif x > 5 : 
    print('Standard Discount Offered ' + str(x) +' percent')
else  :
    print('Low / No Discount Offered ' + str(x) +' percent')


# subsetting
high_discount = data[data['Discount_offered']>60]

#renaming columns, more convienient
shipping = data.rename(columns ={'Warehouse_block':'block',
                                 'Mode_of_Shipment':'mode',
                                 'Customer_care_calls':'calls',
                                 'Customer_rating':'rating',
                                 'Cost_of_the_Product':'cost',
                                 'Prior_purchases':'prior',
                                 'Product_importance':'importance',
                                 'Discount_offered':'discount',
                                 'Weight_in_gms':'weight',
                                 'Reached.on.Time_Y.N':'on_time'})

#pandas subsetting to find biggest issues
issues = np.logical_and(shipping['importance'] == 'high', shipping['on_time'] == 0)
shipping[issues]

# pandas sorting values - by discount and weight
shipping.sort_values(['discount', 'weight'], ascending = [False,True])

# pandas subsetting rows - Highest Discount Shipped Products
shipping[ (shipping['mode'] == 'Ship') & (shipping['discount'] > 60) ]

# pandas subsetting multiple rows on categorical column
shipping[  shipping['block'].isin(['A','B']) ]

# pandas aggregated statistics
shipping['discount'].mean()
shipping['discount'].std()

# agg method with pandas column statistics
def pct40(col):
    return col.quantile(0.4)

def pct60(col):
    return col.quantile(0.6)

shipping['discount'].agg([pct40,pct60])

# Counting cols with pandas & proportions
shipping['block'].value_counts(sort = True)
shipping['mode'].value_counts(sort = True, normalize = True)

# Grouped summary statistics - pandas
shipping.groupby('mode')['discount'].mean()
shipping.groupby('mode')['discount'].agg([pct40,np.mean,pct60])
shipping.groupby(['block','mode'])['discount','weight'].mean()

# Pivot tables in pandas - alternative to groupby statistics (can also be subsetted)
shipping.pivot_table(values = 'discount', index = 'mode', aggfunc = [np.mean, np.median])
piv1 = shipping.pivot_table(values = 'discount', index = 'mode', columns = 'block', margins = True)
piv1.loc['Flight':'Road','A':'C']


# Bar plots with groupby 
on_time_rating = shipping.groupby('block')['on_time'].mean()
on_time_rating.plot(kind='bar', title = 'Proportion on time by block', rot = 0)
plt.show()

# Scatter relationship
a_med = shipping[np.logical_and(shipping['block'] == 'A', shipping['importance'] == 'medium')]
a_med.plot(x='cost',y='discount', kind='scatter', alpha = 0.8, marker = '.', s=7)
plt.show()

# Overlayed histograms
shipping[shipping['block']=='F']['cost'].hist(bins=30)
shipping[shipping['block']=='A']['cost'].hist(bins=30)
plt.legend(['Block F','Block A'])
plt.show()



# Adding a new column to data & investigating via a histogram
shipping['discount_value'] = shipping['discount']  * shipping['cost']
disc = shipping['discount_value']
plt.hist(disc,bins=30,facecolor='g', alpha = 0.6)
plt.grid(True)
plt.xlabel('Discount Value - GBP')
plt.ylabel('Count')
plt.title('Distribution of total discount value offered')
plt.xticks([0,2500,5000,7500,10000,12500,15000,17500],['0','2.5k','5k','7.5k','10k','12.5k','15k','17.5k'])
plt.show()

## User definaed function - Annoyance Factor / Running that function on customer order #43, and #54
def annoy(y): 
    """Returns the annoyance factor for a particular order"""
    if y <0:
        raise ValueError('y must be positive')
        raise TypeError('y must be a valid customer reference number')
    try: 
        annoyance_factor = (shipping.iloc[y]['calls']) * (1 / shipping.iloc[y]['rating']) 
        print(annoyance_factor)
    except TypeError:
        print('y must be a valid customer reference number')

annoy(43)
annoy(54)
annoy('cust54')
annoy(-56)

## Lambda function version of this 
annoy_l = lambda y : (shipping.iloc[y]['calls']) * (1 / shipping.iloc[y]['rating']) 

# Mapping for applying this function to all element of perhaps a directors list
list_dir = [4,6,34,57,65]
Annoy_Factor_list_dir = map(annoy_l, list_dir)
print(list(Annoy_Factor_list_dir))

# Lambda function with reduce
from functools import reduce
cust = [45,65]
avg_disc = reduce(lambda x,y:  (shipping.iloc[x]['discount']+shipping.iloc[y]['discount'])/2, cust)
print(avg_disc)                                                                      
                                                    
# for loop to analyse count data in a data frame
mode_count = {}
mode_col = shipping['mode']

for entry in mode_col:
    if entry in mode_count.keys():
        mode_count[entry] = mode_count[entry]+1
    else: 
        mode_count[entry] = 1
print(mode_count)


# Using lambda functions to filter results 
res = filter( lambda x :  x > 17500 , shipping['discount_value'])
print(list(res))

