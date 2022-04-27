from flask import Blueprint

from app.controllers.category_controller import create_category, delete, retrieve, upgrade

bp = Blueprint('category', __name__, url_prefix='/categories')

bp.post('')(create_category)
bp.get('')(retrieve)
bp.patch('/<int:_id>')(upgrade)
bp.delete('/<int:_id>')(delete)