from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#Init app
app = Flask(__name__)
#so that flask doesn't swallow error messages
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config.from_object('config')


#Init db
db =SQLAlchemy(app)

from app import Student, models