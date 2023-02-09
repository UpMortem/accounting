import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


class PredictCategory():

    def __init__(self):
        # Read in the data into two separate pandas dataframes
        vendors = pd.read_csv("vendor.list", header=None, names=["Vendor"])
        labels = pd.read_csv("labels.list", header=None, names=["Label"])
 
        # Combine the data into a single dataframe
        df = pd.concat([vendors, labels], axis=1)
 
        # Split the data into training and testing sets
        train_df = df[:int(0.8 * len(df))]
        test_df = df[int(0.8 * len(df)):]
 
        # Create a pipeline for transforming the text data and training a logistic regression model
        self.model = Pipeline([
            ('vectorizer', TfidfVectorizer()),
            ('classifier', LogisticRegression())
        ])
 
        # Fit the model on the training data
        self.model.fit(train_df["Vendor"], train_df["Label"])
 
        # Evaluate the model on the testing data
        accuracy = self.model.score(test_df["Vendor"], test_df["Label"])
        print("Accuracy:", accuracy)

    def predict(self, string):
      return self.model.predict([string])[0]
# Example usage
"""
    # Read in the data from the new vendors file
    vendors2 = pd.read_csv("vendors2.list", header=None, names=["Vendor"])

    # Use the trained model to make predictions on the new vendors data
    predictions = model.predict(vendors2["Vendor"])

    # Add the predictions to the vendors2 dataframe
    vendors2["Predicted Label"] = predictions

    # Print the predictions
    print(vendors2["Vendor"][100])
    print(vendors2["Predicted Label"][100])
"""
