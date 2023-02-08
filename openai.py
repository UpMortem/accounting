# Test code to call OpenAI
import requests
import openai
OPENAI_API_KEY = "X"
INPUT = "ADYEN FBO DES:EDI PYMNTS ID:TX10994252700XT INDN:PORTER RANCH SUBWAY IN CO ID:WFBADYENA1 CCD PMT INFO:REF*TN*TX10994252700XT\NTE*INV*SW US 846 38 ZBYPFP676,txid\"
# Function to get the accounting type from GPT-3
def get_account_type(input_str):
    url = 'https://api.openai.com/v1/engines/davinci/completions'
    headers = {'Authorization': "Bearer " + OPENAI_API_KEY}
    data = {'prompt': "What is the Quicken accounting type of: " + input_str, 'max_tokens': 10, 'temperature': 0.7}
    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['text']

print(get_account_type("AMAZON WEB SERVICES"))
