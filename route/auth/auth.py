from flask import Blueprint, redirect, render_template, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from ...Form import LoginForm, RegisterForm  # 导入自定义的登录表单
from ...models import User, Role

mod = Blueprint('auth', __name__, url_prefix='/auth')


@mod.route('/login', methods=['GET', 'POST'])
def login():
    if not current_user.is_authenticated:  # 用户未登录
        form = LoginForm()
        next_point = request.args.get('next')
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is not None and user.verify_password(form.password.data):  # 校验成功
                login_user(user, form.remember_me.data)
                if next_point is None or not next_point.startswith('/'):
                    next_point = url_for('index.index')
                return redirect(next_point)  # 从logout界面跳转而来的会跳回导致一次无用的登录，这种zz操作不做处理
            flash('Invalid username or password.')

        return render_template('auth/login.html', form=form, next=next_point)
    else:
        return redirect(url_for('index.index'))  # 用户已登录，发往首页


# 对本路由不做登录检测，避免自动跳转到login路由而导致无效登录
@mod.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index.index'))


@mod.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        if current_user.is_anonymous or current_user.role.name != 'Admin':  # 只有管理员才能注册
            flash('暂未开放注册，敬请期待。')
            return redirect(url_for('index.index'))
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:  # 存在同名用户
            flash('该用户名已被注册')
            return redirect(url_for('auth.register'))
        # 具备管理员权限 and 不重名
        # 开始注册

        admin = Role.query.filter_by(name='Ordinary').first()
        register_user(User(username=form.username.data,
                                      role=admin,
                                      password=form.password.data))
        # 校验
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            flash('注册成功')
            return redirect(url_for('index.index'))
        else:
            flash('发生未知错误，无法注册')
            return redirect(url_for('auth.register'))
    return render_template('auth/register.html', form=form)


def register_user(new_user):
    from ... import db
    db.session.add(new_user)
    db.session.commit()

    # 创建用户文件夹
    import os
    import shutil
    srcDir = 'static/u/user_temp'  # 用户文件夹模版
    dstDir = 'static/u/' + str(new_user.id)  # 新用户文件夹

    if os.path.exists(dstDir):
        print('异常！！！ 已存在该用户文件夹 ')
        shutil.rmtree(dstDir)
    # 开始拷贝文件夹
    shutil.copytree(srcDir, dstDir)
