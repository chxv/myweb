# run the app
# with python 3.6.4


from . import app
# from flask_script import Manager, Shell

app = app
# app = create_app()


# def make_shell_context():
#     '''直接导入待会在shell中需要用到的所有变量'''
#     return dict(app=app, db=db, User=models.User, Role=models.Role)

#
# manager = Manager(app)
# manager.add_command('shell', Shell(make_context=make_shell_context))  # 添加导入
#
# # 运行
# manager.run()
# app.run(debug=True)



