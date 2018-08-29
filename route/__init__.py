# this package is define all of route

# mod in package
from .auth import mod as auth_mod
from .u import mod as u_mod
# mod in file
from .error import mod as error_mod
from .general import mod as general_mod


def register_all_route(app):
    '''将当前包中所有路由蓝本进行注册'''
    app.register_blueprint(auth_mod)
    app.register_blueprint(u_mod)
    app.register_blueprint(error_mod)
    app.register_blueprint(general_mod)





