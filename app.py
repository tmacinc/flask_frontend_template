from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, PasswordField, DateField, BooleanField, SelectField
from wtforms.validators import DataRequired, NumberRange, Email, EqualTo, InputRequired
from waitress import serve
from queue import Queue
from threading import Thread
from datetime import datetime, timedelta
from time import sleep
import json
import random

# The above are basics for the framework, db integration and a production wsgi server

#--- Flask and SQLAlchemy configuration ---


app = Flask(__name__)   # This tells the framework that we are using this app.py and initializes the framework
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # This is the db info. to use the mysql use 'mysql://u_TestCell:stayconnected@192.168.0.202/test' This is all that needs to change to switch to a different db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # This suppresses warnings from SQLAlchemy that are annoying. Everyone does this
app.config['SECRET_KEY'] = 'Add_a_key_here' # This is used for to create a signed cookie for the app, so the browser session is harder to tamper with.
db = SQLAlchemy(app)    # This creates the db object and binds it to the flask session.

#--- Settings file --- Used for anything related to the config of the app. Gets read on loading

with open('settings.json') as json_file:
    settings = json.load(json_file)

variables = {}
for key, value in settings['variables'].items():
    variables[key] = value

#--- DB Models --- Used by Flask-SQLAlchemy to represent the db as an object https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/

class table(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    item = db.Column(db.String(512), unique = False)

db.create_all() # Function which will check if the table exists and create it if it doesn't

#--- Forms --- Used by WTForms to create the form model. See https://wtforms.readthedocs.io/en/3.0.x/

class sample_form(FlaskForm):
    text_input = StringField('Enter Some text', validators=[DataRequired()])
    submit = SubmitField('Submit')

#--- Variables --- Variables used throughout

variable = 8

#--- Normal Functions --- Standard Python functions used for whatever

def add_entry_to_db(entry):
    db.session.add(entry)
    try:
        db.session.commit()
        print("Results save to db")
    except:
        db.session.rollback()
        print("Error writing to db, results lost")

def get_last_entry_from_db():
    entry = table.query.order_by(table.id.desc()).first() # See https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/ for query options. Filter, filter_by etc
    return entry

def get_all_entries_from_db():
    entries = table.query.all()
    return entries

#--- Route Functions --- These functions run when the url is navigated to in the browser

@app.route('/', methods=['GET', 'POST']) # Decorator that makes this function a route function on address '/'
def index():
    if request.method == 'GET':
        return render_template('index.html', variables = variables) # This will render the template 'index.html' in the templates folder and pass it variable as template_variable.

#------------------- Data routes used by JQuery ------------------------------------------------------------------------

@app.route('/_update_page_variables')                            #Accepts variables list from js and returns current values. 
def update_page_data():
    variables_requested = list(request.args.to_dict().keys())
    data = {}
    #print(f'Received request to get current value of {variables_requested}')
    for variable in variables_requested:
        if variable in variables.keys():
            data[variable] = variables[variable]
    #print(data)
    return jsonify(ajax_data=data)

@app.route('/_set_variable_value')                                 #Accepts requested control variable from user and sends values to background task.
def set_variable_value():
    variable_to_set = request.args.to_dict()
    variable = list(request.args.to_dict().keys())
    variable_name = variable[0]
    print("Received request to update setting: " + variable_name + " to new value: " + variable_to_set[variable_name])
    queue.put({"update_variable": variable_to_set})
    return jsonify(ajax_response="Received variable -> value: " + str(variable_name) + " -> " + str(variable_to_set[variable_name]))

#--------------------- Background Task - This Parallel function to the Flask functions. Used for managing daq, calling threads with control functions etc. Will run without client connected.

def background_tasks(queue=Queue): 
    print("Background thread started")
    t_now = datetime.now()
    t_next = t_now + timedelta(seconds=1)
    while True:
        while t_now < t_next:                               # runs at higher frequency (Event based execution using queue etc.)
            if not queue.empty(): # process queue
                task = queue.get()
                for key in task.keys():
                    if key == "update_variable":
                        for variable, value in task[key].items():
                            variables[variable] = value
            variables['variable_2'] = random.randint(0,100)
            t_now = datetime.now()
            sleep(0.01)
        t_next = t_next + timedelta(seconds=1)              # runs every 1 second (Slower tasks, reading daq etc)
        t_now = datetime.now()

#--------------------- Initialize background thread --------------------------------------------------------------------

queue = Queue()
background = Thread(target=background_tasks, args=(queue,))
background.daemon = True
background.start()

#--- Running the app --- you can run this with 'flask run' as a development option. Using 'python app.py' will run using the option below

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)    # calls the flask development option with options to run on all available IPs in debug mode (this auto restarts when changes are detected)
    #serve(app, port=5000) # This will run on a production wsgi server using waitress
    #waitress is a decent production server for windows
    #gunicorn is a great option for linux