from flask import url_for, render_template, make_response, redirect, abort, jsonify, request, send_file
from icoin import app
from icoin.api import api

@api.route('/version', methods=['GET'])
def version():
    return jsonify(version=app.config['VERSION'])


