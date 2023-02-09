import numpy as np
import csv
import re
import requests
import time
from categories import CATEGORIES
from gpt_category_prediction import PredictCategory

OPENAI_API_KEY = "X"
cache = dict()

# Function to remove lines starting with "Check"
def remove_check(input_str):
    if input_str[:5] == 'Check':
        return ""
    else:
        return input_str

def has_check(input_str):
    if input_str[:5] == 'Check':
        return True
    else:
        return False

# Function to remove extra characters from second column
def remove_extra(input_str):
    return re.sub('[^A-Z]','',input_str)

# Function to get the accounting type
def get_category_type(predictor, input_str):
   return predictor.predict(input_str)

def get_merchant_name(input_str):
    longest = ""
    current = ""
    for char in input_str:
        if char.isalpha() or char == " ":
            current += char
            if len(longest) < len(current):
                longest = current
        else:
            current = ""
    return longest



# Main program
predictor = PredictCategory()
features = []
with open("transactions.csv") as csv_file, open("withdrawal_tab.csv", "w") as output_file:
    csv_reader = csv.reader(csv_file, delimiter=",")

    output_writer = csv.writer(output_file, delimiter=",")

    line_count = 0
    for row in csv_reader:
        if line_count > 8 and float(row[2]) > 0.0:
            row[1] = get_merchant_name(row[1])
            row[3] = float(row[2])
            row[2] = get_category_type(predictor, row[1])
            # Don't include any checks for withdrawals
            if has_check(row[1]):
                pass
            else:
                output_writer.writerow(row)
        line_count += 1
