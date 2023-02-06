import np
import sklearn
from sklearn import linear_model
from sklearn import preprocessing
#Import the necessary libraries
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

# Get the vendors
# Open the file with read only
file = open("vendor.list", "r")

# Create an empty array
arr = []

# Traverse through the file line by line and add each line to the array
for line in file: 
    # Remove the trailing newline character
    line = line.rstrip("\n")
    # Add the line to the array
    arr.append(line)

# Close the file
file.close()
strings = arr

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

#Print the one-hot encoded values
print(one_hot_encoded_values)
one_hot_encoded_values = np.array(one_hot_encoded_values)
print(one_hot_encoded_values)

#Map the encoding back to the original strings
original_strings = le.inverse_transform(numerical_values)

#Print the original strings
print(original_strings)

features = one_hot_encoded_values

# Open the file with read only
file = open("labels.list", "r")

# Create an empty array
arr = []

# Traverse through the file line by line and add each line to the array
for line in file: 
    # Remove the trailing newline character
    line = line.rstrip("\n")
    # Add the line to the array
    arr.append(line)

# Close the file
file.close()
labels = arr

#Create a model using scikit-learn
model = linear_model.LogisticRegression()

#Train the model using the fit method
model.fit(features, labels)

#Make predictions using the predict method
print(features[:5])
prediction = model.predict(features[:5])
print(labels[:5])
#Print the predictions
print(prediction)

