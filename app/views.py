from flask import Flask, render_template
from .forms import RegisterForm
from app import app

@app.errorhandler(404)
def not_found(error):
	return "Sorry, you might be in the wrong place!", 404

@app.errorhandler(500)
def internal_server_error(error):
	return "Whoops, what just happened? We'll get on it.", 500

@app.route("/")
@app.route("/index")
def index():
	user = {'name': 'Jackie Luo'}
	return render_template("index.html",
							title = "Home",
							user = user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('You registered and are now logged in. Welcome!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)