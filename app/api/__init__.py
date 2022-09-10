from app import app
from app.api.user import user
from app.api.event import event

app.register_blueprint(user)
app.register_blueprint(event)

from app.api import error_handler
