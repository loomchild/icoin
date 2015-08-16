import time
from flask import redirect, render_template, request, url_for, flash, abort, send_file
from flask_bootstrap import Bootstrap
from flask_security.core import current_user
from flask_security.decorators import login_required
from icoin.util import to_uuid
from icoin.core.image import get_image
from icoin.core.db import db
from icoin.core.model import User, Page, Pledge, Claim
from . import gui
from .form import CreatePledgeForm, ClaimPageForm


@gui.record_once
def record_once(state):
    app = state.app
    Bootstrap(app)
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True

@gui.context_processor
def utility_processor():
    return dict(current_user=current_user)

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
    
    #TODO: convert to Jinja
    html = '<a href="{0}"><img src="{1}" alt="{2}€"/></a>'.format(
            page_url, image_url, pledge.amount)
    markdown = "[![{0}€]({1})]({2})".format(pledge.amount, image_url, page_url)
    
    return render_template('pledge.html', html=html, markdown=markdown)

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
    #TODO: add global id UUID validation
    page_id = to_uuid(page_id)
    if not page_id:
        abort(404)

    page = db.session.query(Page).get(page_id)

    if not page:
        abort(404)

    claim = db.session.query(Claim).filter_by(
            page_id=page_id, user_id=current_user.user_id).first()

    pledges = db.session.query(Pledge).filter_by(page_id=page_id).all()
    amount = sum(map(lambda pledge: pledge.amount, pledges))

    form = ClaimPageForm()
    if form.validate_on_submit():
        if form.claim.data:
            #TODO: convert to business logic actions, send emails, etc.
            # maybe directly in model, with constructors?
            claim = Claim(current_user, page)
            db.session.add(claim)
            db.session.commit()
            flash("You have claimed the page")
        else:
            return redirect(page.url)

    return render_template('page.html', form=form, url=page.url, amount=amount, claim=claim)
