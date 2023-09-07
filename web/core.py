from flask import render_template

from web import app


@app.errorhandler(404)
def page_not_found(e):
    return render_template('core/404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('core/500.html'), 500
