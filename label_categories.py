import np
import sklearn
from sklearn import linear_model
from sklearn import preprocessing
#Import the necessary libraries
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

def encode_strings(strings):
    '''Encode a list of strings into numerical and one-hot encoded values'''
    #Create an LabelEncoder object
    le = LabelEncoder()
    #Fit the LabelEncoder with the strings
    le.fit(strings)
    #Transform the strings into numerical values
    numerical_values = le.transform(strings)
    #Create an OneHotEncoder object
    enc = OneHotEncoder()
    #Fit the OneHotEncoder with the numerical values
    enc.fit(numerical_values.reshape(-1,1))
    #Transform the numerical values into one-hot encoded values
    one_hot_encoded_values = enc.transform(numerical_values.reshape(-1,1)).toarray()
    one_hot_encoded_values = np.array(one_hot_encoded_values)
    #Map the encoding back to the original strings
    original_strings = le.inverse_transform(numerical_values)
    return one_hot_encoded_values, le

def build_model(features, labels):
    '''Build a logistic regression model'''
    #Create a model using scikit-learn
    model = linear_model.LogisticRegression()
    #Train the model using the fit method
    model.fit(features, labels)
    return model

def make_prediction(model, features):
    '''Make predictions using the logistic regression model'''
    prediction = model.predict(features)
    return prediction

def read_vendors():
    '''Read in "vendor.list" and create an array of strings'''
    #Open the file with read only
    file = open("vendor.list", "r")
    #Create an empty array
    arr = []
    #Traverse through the file line by line and add each line to the array
    for line in file:
        #Remove the trailing newline character
        line = line.rstrip("\n")
        #Add the line to the array
        arr.append(line)
    #Close the file
    file.close()
    return arr

def read_labels():
    '''Read in "labels.list" and create an array of strings'''
    #Open the file with read only
    file = open("labels.list", "r")
    #Create an empty array
    arr = []
    #Traverse through the file line by line and add each line to the array
    for line in file:
        #Remove the trailing newline character
        line = line.rstrip("\n")
        #Add the line to the array
        arr.append(line)
    #Close the file
    file.close()
    return arr

strings = read_vendors()

one_hot_encoded_values, le = encode_strings(strings)
features = one_hot_encoded_values

labels = read_labels()

#Create a model using scikit-learn
model = build_model(features, labels)

prediction = make_prediction(model, features[:10])
print(prediction)
# Map the encoding back to the original strings

# Zip the original strings and the predictions
zipped_list = zip(strings[:10], prediction[:10])

# Print the zipped list
print(list(zipped_list))
