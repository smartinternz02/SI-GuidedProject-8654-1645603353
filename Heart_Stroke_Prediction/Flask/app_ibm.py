from flask import Flask, request,render_template
import joblib
import numpy as np
import requests


app = Flask(__name__)

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "Z3uWFvZLMkCxrP7McP2otDti2HgOYk-CoiQ1YbhqbIwi"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

@app.route('/')
def predict():
    return render_template('Manual_predict.html')

@app.route('/y_predict',methods=['POST'])
def y_predict():
    g= request.form["Gender"]
    if (g == 'f'):
        g1,g2,g3=1,0,0
    if (g == 'm'):
        g1,g2,g3=0,1,0
    if (g == 'o'):
        g1,g2,g3=0,0,1
    age= request.form["Age"]
    q= request.form["Hypertension"]
    if (q == 'n'):
        q=0
    if (q == 'y'):
        q=1
    hd= request.form["heart_disease"]
    if (hd == 'n'):
        hd=0
    if (hd == 'y'):
        hd=1    
    em= request.form["ever_married"]
    if (em == 'n'):
        em=0
    if (em == 'y'):
        em=1   
    wt= request.form["work_type"]
    if (wt == 'ch'):
        wt1,wt2,wt3,wt4,wt5 = 1,0,0,0,0
    if (wt == 'gvt'):
        wt1,wt2,wt3,wt4,wt5 = 0,1,0,0,0
    if (wt == 'unemp'):
        wt1,wt2,wt3,wt4,wt5 = 0,0,1,0,0   
    if (wt == 'pvt'):
        wt1,wt2,wt3,wt4,wt5 = 0,0,0,1,0
    if (wt == 'self'):
        wt1,wt2,wt3,wt4,wt5 = 0,0,0,0,1
    rt= request.form["Residence_type"]
    if (rt == 'rural'):
        rt=0
    if (rt == 'urban'):
        rt=1  
    agl= request.form["avg_glucose_level"]
    bmi= request.form["BMI"]
    sm= request.form["smoking_status"]
    if (sm == 'for'):
        sm1,sm2,sm3=1,0,0
    if (sm == 'ns'):
        sm1,sm2,sm3=0,1,0
    if (sm == 's'):
        sm1,sm2,sm3=0,0,1    
        
    inp= np.array([g1,g2,g3,wt1,wt2,wt3,wt4,wt5,sm1,sm2,sm3,age,q,hd,em,rt,agl,bmi])
    print(inp)
    
    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": [["g1","g2","g3","wt1","wt2","wt3","wt4","wt5","sm1","sm2","sm3","age","q","hd","em","rt","agl","bmi"]], "values": [[0,1,0,0,0,1,0,0,1,0,0,67,0,1,1,1,168.32,36.6]]}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/566bf3ca-c249-4e0e-a528-c26461ae2b8a/predictions?version=2022-03-05', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    #print("Scoring response")
    print(response_scoring.json())
    op = response_scoring.json()
    pred= op["predictions"][0]['values'][0][0]
    print(pred)
        
    #pred = model.predict([inp])   
    #print(pred)    

    if(pred==0):
        result="no chances of stroke"
    else:result="chances of stroke"
    
    return render_template('Manual_predict.html', \
                           prediction_text=('There are \
                                            ',result))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
    
