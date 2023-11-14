# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 18:25:20 2023

@author: Dan
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
import sklearn
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

# This script shows a KNN classifier approach to try to predict whether a particular
# parcel due to be delivered by a logistics company will arrive on time. 
# Use Case - A logistics company could highlight their weaknesses of operation.
# Use Case - Additional focus put onto those packages at risk of being late.
# Works on the premise that the number of calls, the weight and cost of the 
# parcel is an indicator of whether the parcel will be on time. 
# This would hold true were the logistic company to have an issue with a particular 
# type of parcel  ,  eg very small or say extra large parcels. 

filename = 'shippingdata.csv'
data = pd.read_csv(filename, index_col = 0)

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

y = shipping['on_time']
X = shipping[['calls','rating','cost','prior','weight']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=15, stratify=y)

knn = KNeighborsClassifier(n_neighbors=4)
knn.fit(X_train,y_train)
knn.score(X_test,y_test)

# Looping to test many neighbor numbers
neighbors = np.arange(1, 9)
train_accuracy = np.empty(len(neighbors))
test_accuracy = np.empty(len(neighbors))

# Loop over different values of k
for i, k in enumerate(neighbors):
    # Setup a k-NN Classifier with k neighbors: knn
    knn = KNeighborsClassifier(n_neighbors=k)

    # Fit the classifier to the training data
    knn.fit(X_train, y_train)
    
    #Compute accuracy on the training set
    train_accuracy[i] = knn.score(X_train, y_train)

    #Compute accuracy on the testing set
    test_accuracy[i] = knn.score(X_test, y_test)

# Generate plot
plt.title('k-NN: Varying Number of Neighbors')
plt.plot(neighbors, test_accuracy, label = 'Testing Accuracy')
plt.plot(neighbors, train_accuracy, label = 'Training Accuracy')
plt.legend()
plt.xlabel('Number of Neighbors')
plt.ylabel('Accuracy')
plt.show()

# Results show a plateau of accuracy around the 67% mark of test accuracy for 
# K increasing from 2 to 8. A further step could be to use lambda regression, 
# to highlight particuarly important features for predicting whether a parcel
# is on time, and try running models with less & more variables to improve accuracy. 

# Additionally we could try a bootstrapping approach of cross validation to 
# again increase the reliability of our test here. 

# The important question to ask is, as a business does a 67% accuracy level 
# actually improve the profitability in any way.  Would you make business
# decisions at that level of confidence.  The answer may well be no in this case. 
