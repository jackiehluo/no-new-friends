from flask import render_template, Blueprint
from flask.ext.login import login_required

from app.decorators import check_confirmed
from app.models import User
from config import USERS_PER_PAGE

main_blueprint = Blueprint('main', __name__,)


@main_blueprint.route('/')
@main_blueprint.route('/index')
@main_blueprint.route('/index/<int:page>')
@login_required
@check_confirmed
def home(page=1):
    users = User.query.paginate(page, USERS_PER_PAGE, False)
    return render_template('main/index.html',
                           users=users)