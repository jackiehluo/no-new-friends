from flask import Flask, render_template, request
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter
import requests

def create_app():
	app = Flask(__name__)

	db = SQLAlchemy(app)
    mail = Mail(app)

    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)

        # User authentication information
        username = db.Column(db.String(50), nullable=False, unique=True)
        password = db.Column(db.String(255), nullable=False, server_default='')
        reset_password_token = db.Column(db.String(100), nullable=False, server_default='')

        # User email information
        email = db.Column(db.String(255), nullable=False, unique=True)
        confirmed_at = db.Column(db.DateTime())

        # User information
        active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
        first_name = db.Column(db.String(100), nullable=False, server_default='')
        last_name = db.Column(db.String(100), nullable=False, server_default='')

    db.create_all()

    db_adapter = SQLAlchemyAdapter(db, User)
    user_manager = UserManager(db_adapter, app)

	@app.route("/")
	def start():
    	return render_template("start.html")

	@app.route('/search', methods = ["GET", "POST"])
	def search():
		if request.method == "POST":
			url = "https://api.github.com/search/repositories?q=" + request.form["user_search"]
			print request.form
			response = requests.get(url)
			response_dict = response.json()
			return render_template("results.html", api_data = response_dict)
		else:
			return render_template("search.html")

	@app.route('/findfriends')
    @login_required
    def find_friends():
    	return render_template("findfriends.html")

	@app.errorhandler(404)
	def not_found(error):
		return "Sorry, you might be in the wrong place!", 404

	@app.errorhandler(500)
	def internal_server_error(error):
		return "Whoops, what just happened? We'll get on it.", 500

if __name__ == '__main__':
	app.run(host = '0.0.0.0')