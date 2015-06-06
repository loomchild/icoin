import time
from flask import redirect, render_template, request, url_for, flash, abort, send_file
from flask_bootstrap import Bootstrap
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
from icoin.core.image import get_image
from icoin.core.db import db
from icoin.core.model import User, Page, Pledge
from . import gui
from .form import LoginForm, RegisterForm, CreatePledgeForm, ClaimPageForm


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = '.login'


@gui.record_once
def record_once(state):
    app = state.app
    login_manager.init_app(app)
    Bootstrap(app)
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)

@gui.context_processor
def utility_processor():
    return dict(current_user=current_user)

@gui.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            next = request.values.get('next')
            return redirect(next or url_for(".create_pledge"))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)

@gui.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect("/")

@gui.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(form.email.data, form.name.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account has been registered, please log in.')
        return redirect(url_for(".login"))
    return render_template('register.html', form=form)


@gui.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@gui.route("/pledge.html", methods=['GET', 'POST'])
@login_required
def create_pledge():
    form = CreatePledgeForm()
    if form.validate_on_submit():
        #TODO: support update existing pledge, block duplicates
        url = form.url.data
        amount = form.amount.data
 
        page = db.session.query(Page).filter_by(url=url).first()
        if not page:
            page = Page(url)
            db.session.add(page)

        pledge = Pledge(current_user, page, amount)
        db.session.add(pledge)
        db.session.commit()   

        return redirect(url_for('.pledge', pledge_id=str(pledge.pledge_id)))
    return render_template('create_pledge.html', form=form)

@gui.route("/pledge/<pledge_id>.html", methods=['GET', 'POST'])
@login_required
def pledge(pledge_id):
    # TODO: check if logged user, maybe in view
    pledge = db.session.query(Pledge).get(pledge_id)
    image_url = url_for('.pledge_image', pledge_id=pledge_id, _external=True)
    page_url = url_for('.page', page_id=pledge.page_id, _external=True)
    image = "[![{0}€]({1})]({2})".format(pledge.amount, image_url, page_url)
    return render_template('pledge.html', image=image)

#TODO: move to API
@gui.route("/pledge/<pledge_id>.png", methods=['GET'])
def pledge_image(pledge_id):
    pledge = db.session.query(Pledge).get(pledge_id)

    response = send_file(get_image(pledge.amount), mimetype='image/png')
    
    response.cache_control.no_cache = True
    response.cache_control.max_age = None
    response.cache_control.public = False
    del response.headers['Expires']
    #response.headers['Last-Modified'] = 'Mon, 17 Feb 2014 15:21:20 GMT'
    response.headers['Pragma'] = 'no-cache'
    response.headers['ETag'] = '"{}"'.format(int(round(time.time() * 1000)))

    return response

#TODO: add domain to page url to easily identify fraud
@gui.route("/page/<page_id>.html", methods=['GET', 'POST'])
@login_required
def page(page_id):
    page = db.session.query(Page).get(page_id)
    pledges = db.session.query(Pledge).filter_by(page_id=page_id).all()
    amount = sum(map(lambda pledge: pledge.amount, pledges))

    form = ClaimPageForm()
    if form.validate_on_submit():
        if form.yes.data:
            flash("You have claimed the page")
        else:
            flash("Nothing claimed")
    return render_template('page.html', form=form, url=page.url, amount=amount)

