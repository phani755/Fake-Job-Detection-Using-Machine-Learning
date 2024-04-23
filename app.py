from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import myfile as mf
#import sys
#sys.path.append('F:\COLLEGES WORKSPACE\KCEA\PROJECTS\06 FAKE JOB LISTING')



app = Flask(__name__)


model = pickle.load(open('fake_job_listing_rf.pkl', 'rb'))
@app.route('/')
def index():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        job_id = request.form['job_id']
        title=request.form['title']
        location=request.form['location']
        department=request.form['department']
        salary_range=request.form['salary_range']
        industry=request.form['industry']

        lst = [job_id,title,location,department,salary_range,industry]
        data = [{'job_id': job_id, 'title': title, 'location':location,'department':department,'salary_range':salary_range,'industry':industry}]  

        #print("%%%%%%%%%%%%%%%%%%%%%%%",lst)
  
        # Calling DataFrame constructor on list
        # with indices and columns specified
        df = pd.DataFrame(data)
        print("*********************************************************************************")
        print("\n")
        print(df)
        print("\n")
        print("*********************************************************************************")
        
        #print("######### JOB ID ",type(job_id))
        
        le = LabelEncoder()
        #job_id1= le.fit_transform(df['job_id'])
        title1= le.fit_transform(df['title'])
        location1= le.fit_transform(df['location'])
        department1= le.fit_transform(df['department'])
        salary_range1= le.fit_transform(df['salary_range'])
        industry1= le.fit_transform(df['industry'])
        function1= le.fit_transform(df['department'])

        
        prediction=model.predict([[job_id,title1,location1,department1,salary_range1,industry1,function1]])
        prediction1=model.predict([[1,1,1,1,1,1,1]])
        print("PRED ",prediction)
        print("PRED1 ",prediction1)
        output=round(prediction[0],2)
        ind_name=str(industry)
        jobList=mf.getFieldPlaces(industry,location,)
        output=jobList
        print("OUTPUT : ",output)
        
        if output==1:
            return render_template('index.html',prediction_error="Hey It's Fake")
        else:
            return render_template('index.html',prediction_success="Hurray its Real You can Continue....".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)

