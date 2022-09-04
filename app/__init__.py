from flask import Flask
from flask_talisman import Talisman

app = Flask(__name__)

# Configuration
from app.config import Configuration
app.config.from_object(Configuration)

# Setting up avoid strict slashes
app.url_map.strict_slashes = False

# Security
from flask_cors import CORS
CORS(app, supports_credentials=True)

# from flask_talisman import Talisman
Talisman(app)

# Database init
from app.model import db
from app.model.database import *

# database migration
from flask_migrate import Migrate
migrate = Migrate(app, db)

# db.drop_all()
db.create_all()

# Routes
from app import api
