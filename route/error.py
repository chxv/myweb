from flask import Blueprint, render_template

mod = Blueprint('error', __name__, url_prefix='/error')


@mod.app_errorhandler(403)
def internal_server_error(e):
    '''Forbidden'''
    return render_template('error/403.html'), 403


@mod.app_errorhandler(404)
def page_not_found(e):
    '''Not Found'''
    return render_template('error/404.html'), 404


@mod.app_errorhandler(405)
def method_not_allowed(e):
    '''Method not allowed'''
    return render_template('error/405.html'), 405


@mod.app_errorhandler(500)
def internal_server_error(e):
    '''Internal server error'''
    return render_template('error/500.html'), 500
