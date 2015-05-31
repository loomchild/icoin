import time

from flask import redirect, render_template, request, url_for, flash, abort, send_file
from flask_bootstrap import Bootstrap

from icoin.core.image import get_image

from . import gui
from .form import CreatePledgeForm, ClaimPageForm



@gui.record_once
def record_once(state):
    app = state.app
    Bootstrap(app)
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True


@gui.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@gui.route("/pledge.html", methods=['GET', 'POST'])
def create_pledge():
    form = CreatePledgeForm()
    if form.validate_on_submit():
        url = form.url
        amount = form.amount.data
        
        pledgeid = "abcdef0123456789"

        return redirect(url_for('.pledge', pledgeid = pledgeid))
    return render_template('create_pledge.html', form=form)

@gui.route("/pledge/<pledgeid>.html", methods=['GET', 'POST'])
def pledge(pledgeid):
    # TODO: check of logged user, maybe in view
    #host = "http://localhost:8080"
    host = "https://icoin.ngrok.io"
    pageid = '9876543210fedcba'
    image = "[![1€]({0}/pledge/{1}.png)]({0}/page/{2}.html)" \
            .format(host, pledgeid, pageid)
    
    return render_template('pledge.html', image=image)

@gui.route("/pledge/<pledgeid>.png", methods=['GET'])
def pledge_image(pledgeid):
    #from pprint import pprint; pprint(vars(request))

    amount = 2
    response = send_file(get_image(amount), mimetype='image/png')
    
    response.cache_control.no_cache = True
    response.cache_control.max_age = None
    response.cache_control.public = False
    del response.headers['Expires']
    #response.headers['Last-Modified'] = 'Mon, 17 Feb 2014 15:21:20 GMT'
    response.headers['Pragma'] = 'no-cache'
    response.headers['ETag'] = '"{}"'.format(int(round(time.time() * 1000)))

    
    return response

#TODO: add domain to page url to easie identify fraud
@gui.route("/page/<pageid>.html", methods=['GET', 'POST'])
def page(pageid):
    #from IPython import embed; embed()
    url = 'http://example.com/page1.html'
    amount = 2
    form = ClaimPageForm()
    if form.validate_on_submit():
        if form.yes.data:
            flash("You have claimed the page")
        else:
            flash("Nothing claimed")
    return render_template('page.html', form=form, url=url, amount=amount)

