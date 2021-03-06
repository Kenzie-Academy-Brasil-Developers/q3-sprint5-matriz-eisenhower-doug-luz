from flask import Blueprint, Flask
from .categories_routes import bp as bp_category
from .tasks_routes import bp as bp_task

bp_api = Blueprint('api', __name__, url_prefix='/api')

def init_app(app:Flask):
    bp_api.register_blueprint(bp_category)
    bp_api.register_blueprint(bp_task)
    
    app.register_blueprint(bp_api)
    