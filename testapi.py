from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

#list all alert in the system
@app.route('/listalert', methods=['GET'])
def listalert():
    r = requests.get('http://localhost:8000/alert')
    json_object = r.json()['alerts']
    return render_template('listalert.html', alerts=json_object)

#edit alert form accept an ID in URL form
@app.route('/editalert/<alertid>', methods=['GET'])
def editalert(alertid):
    #get all users
    r = requests.get('http://localhost:8000/users')
    json_object = r.json()
    users = json_object

    #get alert content
    r = requests.get('http://localhost:8000/alert/'+alertid)
    json_object = r.json()
    #return r.text
    return render_template('update.html', alert=json_object, users=users)

#edit alert process
@app.route('/editalertp', methods=['POST'])
def editalertprocess():
    #alert API addalert need JSON so we need to prepare data in json format
    data = {
              'alert_name': request.form['alertname'],
              'output_format': ','.join(request.form.getlist('alertoutput')),
              'output_recipients': ','.join(request.form.getlist('alertusers')),
              'schedule': request.form['alertschedule'],
              'rule_text': request.form['alertscript'],
          }

    url = "http://localhost:8000/alert/"+request.form['id']

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.put(url, data=json.dumps(data), headers=headers)

    return render_template('addsuccess.html')

#add new alert to system
@app.route('/createalert', methods=['POST'])
def addalert():
    #aeirt API addalert need JSON so we need to prepare data in json format
    data = {
              'alert_name': request.form['alertname'],
              'alert_table': 'eventdrivensignal-mysql-estdiversion',
              'enabled': 1,
              'schedule': request.form['alertschedule'],
              'output_format': ','.join(request.form.getlist('alertoutput')),
              'output_recipients': ','.join(request.form.getlist('alertusers')),
              'rule_text': request.form['alertscript'],
              'schedule': 'updates'
          }

    #return jsonify(data)

    #'rule_text are in form ': 'def findEstNames(df): ',
    url = "http://localhost:8000/alert/add"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data=json.dumps(data), headers=headers)

    return render_template('addsuccess.html')

#del alert not implement yet
@app.route('/delalert', methods=['GET'])
def delalert():
    return "Delete..."

#default page it is add new alert form
@app.route('/')
def index():
    #get all users
    r = requests.get('http://localhost:8000/users')
    json_object = r.json()
    users = json_object

    return render_template('index.html', users=users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
