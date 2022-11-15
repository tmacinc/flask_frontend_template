from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, PasswordField, DateField, BooleanField, SelectField
from wtforms.validators import DataRequired, NumberRange, Email, EqualTo, InputRequired
from waitress import serve

# The above are basics for the framework, db integration and a production wsgi server

#--- Flask and SQLAlchemy configuration ---


app = Flask(__name__)   # This tells the framework that we are using this app.py and initializes the framework
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # This is the db info. to use the mysql use 'mysql://u_TestCell:stayconnected@192.168.0.202/test' This is all that needs to change to switch to a different db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # This suppresses warnings from SQLAlchemy that are annoying. Everyone does this
app.config['SECRET_KEY'] = 'Add_a_key_here' # This is used for to create a signed cookie for the app, so the browser session is harder to tamper with.
db = SQLAlchemy(app)    # This creates the db object and binds it to the flask session.

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
    form = sample_form(meta={'csrf': False})
    if request.method == 'GET':
        return render_template('index.html', template_variable = variable, template_form = form) # This will render the template 'index.html' in the templates folder and pass it variable as template_variable.
    if form.validate_on_submit():
        print(f'Form data received {form.data}')
        print
        entry = table(item = form.data['text_input'])
        add_entry_to_db(entry)
        entries = get_all_entries_from_db()
        data = []
        for entry in entries:
            data.append(entry.item)
        print(data)
        return render_template('result.html', db_data = data)
#--- Running the app --- you can run this with 'flask run' as a development option. Using 'python app.py' will run using the option below

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)    # calls the flask development option with options to run on all available IPs in debug mode (this auto restarts when changes are detected)
    #serve(app, port=5000) # This will run on a production wsgi server using waitress
    #waitress is a decent production server for windows
    #gunicorn is a great option for linux