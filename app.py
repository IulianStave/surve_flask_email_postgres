# Create the virtual environment by running :
"""
in parent folder
       python3 -m venv survenv (replace venv with virtualenv)
activate the virtual environment
go to survenv folder
/survenv/source bin/activate
cd ../surv
pip3 install sqlalchemy
pip3 install flask
pip3 install flask_sqlalchemy

sudo apt-get install python3-setuptools
sudo apt install libpq-dev python3-dev

pip3 install psycopg2
in pgadmin4 create the database before running the script app.py within virtual environment created
then complete the configuration file with email address and password,posgres user, postgres password and database name, table name will be data
the email account will be used to send survey results, it should be configured to allow `Less secure app access`
to create a table in the database height_collector use python
start python3
from app import db
db.create_all()
"""
# from the parent folder surv 
# use virtual\Scripts\activate to run the virtual env
# then run with 

# python3 app.py

# or simply for Windows environment
# py app.py
# use https://www.lfd.uci.edu to download python precompiled libraries (wheels) - on windows
# 
"""
Use sqlalchemy instead of psycopg2 
To upgrade pip use the below command
python3 -m pip install --upgrade pip

pip install Flask-SQLAlchemy
"""

from flask import Flask, render_template, request
#from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from send_emails import send_email

app = Flask (__name__)
config_file = 'survey_db_email.conf'
db_credentials = {
    'postgres_user':'',
    'postgres_password':'',
    'database':'',
    }

#reading configuration credentials
with open(config_file) as file:
    content = file.read().splitlines()
    #print(content)
    #db_credentials.update({content[2]:content[3]})
    db_credentials['postgres_user'] = content[2]
    db_credentials['postgres_password'] = content[3]
    db_credentials['database'] = content[4]
    db_credentials['table_name'] = content[5]

my_db_uri = 'postgresql://{}:{}@localhost/{}'.format(
    db_credentials['postgres_user'],
    db_credentials['postgres_password'],
    db_credentials['database'],
    db_credentials['table_name'])

app.config['SQLALCHEMY_DATABASE_URI']=my_db_uri
db = SQLAlchemy(app)


class Data(db.Model):
    #__tablename__ = "data"
    __tablename__ = db_credentials['table_name']
    id = db.Column(db.Integer, primary_key = True)
    email_ = db.Column(db.String(120), unique = True)
    height_ = db.Column(db.Integer)

    def __init__(self, email_, height_):
        self.email_ = email_
        self.height_ = height_

# to instantiate the table above run Python (Python3) in console
# and there:   
# from app import db
# db.create_all() 
# the script app.py won't be executed, only the db object will be imported
# ensured with the condition:  if __name__ == '__main__'



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods = ["POST"])
def success():
    if request.method =='POST':
        email = request.form["email_name"]
        height = request.form["height"] 
        send_email(email, height)
        #query uses the database model Data which returns how many entries have the same email
        if db.session.query(Data).filter(Data.email_ == email).count() == 0:
            data_for_db = Data(email, height)
            db.session.add(data_for_db)
            db.session.commit()
            return render_template("success.html",email = email, height = height)
    return render_template("index.html",
    text = "Seems like we've got this email address already" )

if __name__ == '__main__':
    #app.debug = True
    app.run(debug = True)
    
