from flask import render_template, Blueprint
from flask.ext.login import login_required


main_blueprint = Blueprint('main', __name__,)


@main_blueprint.route('/')
@login_required
def home():
    return render_template('main/index.html')