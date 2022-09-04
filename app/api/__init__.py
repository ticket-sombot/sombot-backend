from app import app
from app.api.user import user

app.register_blueprint(user)

from app.api import error_handler
