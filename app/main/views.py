from flask import render_template, Blueprint
from flask.ext.login import login_required

from app.decorators import check_confirmed
from app.models import User

main_blueprint = Blueprint('main', __name__,)


@main_blueprint.route('/')
@login_required
@check_confirmed
def home():
    users = User.query.all()
    return render_template('main/index.html',
                           users=users)