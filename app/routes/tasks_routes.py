from flask import Blueprint

from app.controllers.task_controller import create_task, retrieve, upgrade,delete

bp = Blueprint('tasks', __name__, url_prefix='/tasks')

bp.post('')(create_task)
bp.patch('<int:_id>')(upgrade)
bp.delete('<int:_id>')(delete)
bp.get('')(retrieve)