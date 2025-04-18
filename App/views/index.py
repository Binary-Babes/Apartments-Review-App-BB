from flask import Blueprint, render_template
from flask_login import current_user, login_required

index_views = Blueprint('index_views', __name__)

@index_views.route('/', methods=['GET'])
@login_required
def index_page():
    return render_template(
        'index.html',
        is_authenticated=current_user.is_authenticated,
        is_admin=(current_user.is_authenticated and getattr(current_user, 'is_admin', False)),
        current_user=current_user
    )
