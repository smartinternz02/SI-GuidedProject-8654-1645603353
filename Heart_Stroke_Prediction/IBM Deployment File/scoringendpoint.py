import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "Z3uWFvZLMkCxrP7McP2otDti2HgOYk-CoiQ1YbhqbIwi"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"fields": [["g1","g2","g3","wt1","wt2","wt3","wt4","wt5","sm1","sm2","sm3","age","q","hd","em","rt","agl","bmi"]], "values": [[0,1,0,0,0,1,0,0,1,0,0,67,0,1,1,1,168.32,36.6]]}]}

response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/566bf3ca-c249-4e0e-a528-c26461ae2b8a/predictions?version=2022-03-05', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
print(response_scoring.json())
op = response_scoring.json()
pred= op["predictions"][0]['values'][0][0]
print(pred)