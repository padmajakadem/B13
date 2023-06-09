from flask import Flask,render_template,redirect,request
import time
import pyotp
import qrcode
from pymongo import MongoClient
from datetime import datetime

client=MongoClient('localhost',27017)
db=client['B13']
c=db['data']

key="MadhuforGeeksIsBestForEverything"

totp = pyotp.TOTP(key)

app=Flask(__name__)

@app.route('/')
def homePage():
    return render_template('index.html')

@app.route('/dashboard')
def dashboardPage():
    return render_template('dashboard.html')

@app.route('/loginotp',methods=['post'])
def loginotp():
    otp=request.form['otp']
    state=totp.verify(int(otp))
    if state==True:
        return redirect('/dashboard')
    else:
        return render_template('index.html',err='Invalid Otp')

@app.route('/addAccessPoint',methods=['post'])
def addAccessPoint():
    name=request.form['name']
    dept=request.form['dept']
    empid=request.form['empid']
    empmobile=request.form['empmobile']
    print(name,dept,empid,empmobile)
    k={}
    k['ap']=name
    k['department']=dept
    k['empid']=empid
    k['empmobile']=empmobile
    k['timestamp']=str(datetime.now())
    c.insert_one(k)
    return render_template('dashboard.html',res='Access Point Added')

@app.route('/listofaps')
def listofaps():
    data=[]
    for i in c.find():
        dummy=[]
        dummy.append(i['ap'])
        dummy.append(i['department'])
        dummy.append(i['empid'])
        dummy.append(i['empmobile'])
        dummy.append(i['timestamp'])
        data.append(dummy)
    return render_template('listofaps.html',dashboard_data=data,len=len(data))

@app.route('/logout')
def logout():
    return redirect('/')

if __name__=="__main__":
    app.run(host='0.0.0.0',port=5000)