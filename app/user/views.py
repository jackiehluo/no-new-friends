from flask import render_template, Blueprint, url_for, redirect, flash, request, make_response
from flask.ext.login import login_user, logout_user, login_required, current_user
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic
from datetime import datetime

from app import db, bcrypt
from app.decorators import check_confirmed
from app.email import send_email
from app.models import User
from app.token import generate_confirmation_token, confirm_token
from .forms import LoginForm, RegisterForm, ChangePasswordForm, EditForm
from config import CONFIG, SECRET_KEY

user_blueprint = Blueprint('user', __name__,)
authomatic = Authomatic(CONFIG, SECRET_KEY, report_errors=False)


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            major = form.major.data,
            interests=form.interests.data,
            phone=form.phone.data,
            email=form.email.data,
            password=form.password.data,
            confirmed=False
        )
        db.session.add(user)
        db.session.commit()

        token = generate_confirmation_token(user.email)
        confirm_url = url_for('user.confirm_email', token=token, _external=True)
        html = render_template('user/activate.html', confirm_url=confirm_url)
        subject = "Confirm your email for No New Friends!"
        send_email(user.email, subject, html)

        login_user(user)

        flash('A confirmation email has been sent via email.', 'success')
        return redirect(url_for('user.unconfirmed'))

    return render_template('user/register.html', form=form)


@user_blueprint.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for('main.home'))
    flash('Please confirm your account!', 'warning')
    return render_template('user/unconfirmed.html')


@user_blueprint.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('user.confirm_email', token=token, _external=True)
    html = render_template('user/activate.html', confirm_url=confirm_url)
    subject = "Confirm your email for No New Friends!"
    send_email(current_user.email, subject, html)
    flash('A new confirmation email has been sent.', 'success')
    return redirect(url_for('user.unconfirmed'))


@user_blueprint.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('main.home'))


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
                user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash('Invalid email and/or password.', 'danger')
            return render_template('user/login.html', form=form)
    return render_template('user/login.html', form=form)


@user_blueprint.route('/profile/<id>', methods=['GET', 'POST'])
@login_required
@check_confirmed
def profile(id):
    form = ChangePasswordForm(request.form)
    user = User.query.filter_by(id=id).first()
    if user == None:
        flash('We couldn\'t find that user!')
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        if user:
            user.password = bcrypt.generate_password_hash(form.password.data)
            db.session.commit()
            flash('Password successfully changed.', 'success')
            return redirect(url_for('user.profile', id=current_user.id))
        else:
            flash('Password change was unsuccessful.', 'danger')
            return redirect(url_for('user.profile', id=current_user.id))
    return render_template('user/profile.html', form=form, user=user)


@user_blueprint.route('/edit', methods=['GET', 'POST'])
@login_required
@check_confirmed
def edit():
    form = EditForm(request.form)
    user = User.query.filter_by(email=current_user.email).first()
    if form.validate_on_submit():
        if user:
            user.major = form.major.data
            user.interests = form.interests.data
            user.about_me = form.about_me.data
            user.instagram = form.instagram.data
            user.twitter = form.twitter.data
            db.session.commit()
            flash('Profile successfully updated.', 'success')
            return redirect(url_for('user.profile', id=current_user.id))
        else:
            flash('Profile update unsuccessful.', 'danger')
            return redirect(url_for('user.profile', id=current_user.id))
    elif request.method != "POST":
        form.major.data = user.major
        form.interests.data = user.interests
        form.about_me.data = user.about_me
        form.instagram.data = user.instagram
        form.twitter.data = user.twitter
    return render_template('user/edit.html', form=form)


@user_blueprint.route('/<id>/login/<provider_name>/', methods=['GET', 'POST'])
@login_required
@check_confirmed
def social_login(id, provider_name):
    response = make_response()
    result = authomatic.login(WerkzeugAdapter(request, response), provider_name)
    if result:
        if result.user:
            result.user.update()
            user = User.query.filter_by(id=current_user.id).first()
            if user:
                user.facebook = result.user.id
                db.session.commit()
        flash('Facebook added!', 'success')
        return redirect(url_for('user.profile', result=result, id=current_user.id))
    return response


@user_blueprint.route('/contact/<id>')
@login_required
@check_confirmed
def contact(id):
    user = User.query.filter_by(id=id).first()
    first_name = current_user.first_name
    last_name = current_user.last_name
    interests = current_user.interests
    phone = '(%s) %s-%s' % (current_user.phone[:3], current_user.phone[3:6], current_user.phone[6::])
    html = render_template('user/contact.html', first_name=first_name, last_name=last_name,
        interests=interests, phone=phone)
    subject = 'Someone on No New Friends wants to meet you!'
    send_email(user.email, subject, html)
    flash('You just messaged someone!', 'success')
    return redirect(url_for("main.home"))


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.', 'success')
    return redirect(url_for('user.login'))