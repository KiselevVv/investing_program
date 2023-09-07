import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_object(
    os.environ.get('FLASK_ENV') or 'config.DevelopmentConfig')

db = SQLAlchemy(app)

from web.models import Companies

with app.app_context():
    db.create_all()
    db.session.commit()

# import views
from web import views, core
