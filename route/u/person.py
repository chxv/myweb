from flask import Blueprint, redirect, render_template, url_for, flash, request, current_app
from flask_login import login_required, current_user
# from werkzeug.utils import secure_filename
# import os

mod = Blueprint('u', __name__, url_prefix='/u')


@mod.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    from ...models import Article
    from ...func import allowed_file, get_user_config
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if not allowed_file(file.filename, 'Article'):
            flash('File type error!')
            return redirect(request.url)
        if file:

            # 保存文件
            import random
            import datetime
            filename = str(random.randrange(0, 1024, 1)) + datetime.datetime.now().strftime('-%y%m%d%H%M%S%f') + \
                '.' + file.filename.rsplit('.', 1)[1]  # 确保文件安全以及避免同名文件
            upload_folder = f'static/u/{current_user.id}/'   # static/u/<user_id>/filename
            file.save(upload_folder + filename)
            # 保存文件信息到数据库
            new_essay = Article(user_id=current_user.id,
                                title=request.form['title'][:127],
                                synopsis=request.form['about'][:1023],
                                classification=request.form['classification'][0:31],
                                raw_filename=file.filename[0:255],
                                file_name=filename)
            # 时间戳自动使用当前时间，保密secrecy默认为 'secret'
            from ... import db
            db.session.add(new_essay)
            db.session.commit()
            return redirect(url_for('u.home'))

    articles = Article.query.filter_by(user_id=current_user.id).all()
    config_ini = 'info.ini'  # 配置文件名
    conf = get_user_config(f'static/u/{current_user.id}/{config_ini}')  # 获得配置信息
    info = {
        'head_portrait': conf['head_portrait'],  # 头像位置
        'user_id': current_user.id,  # 用户的id
        'nickname': current_user.nickname,  # 昵称
        'signature': current_user.signature,  # 个性签名
        'articles': articles  # 文章列表
    }
    # 用户文件夹 /static/u/<user_id>/
    return render_template('u/home.html', info=info)


@mod.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    from ...models import User
    from ...func import allowed_file, modify_user_config
    if request.method == 'POST':
        # 用户上传个人信息
        # 若包含文件
        if 'file' in request.files:
            file = request.files['file']  # 文件
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if not allowed_file(file.filename, 'Image'):
                flash('File type error!')
                return redirect(request.url)
            if file:
                # 保存文件，更改头像
                import random
                import datetime
                filename = str(random.randrange(0, 1024, 1)) + datetime.datetime.now().strftime('-%y%m%d%H%M%S%f') + \
                    '.' + file.filename.rsplit('.', 1)[1]  # 确保文件安全以及避免同名文件
                upload_folder = f'static/u/{current_user.id}/'  # static/u/<user_id>/filename
                file.save(upload_folder + filename)
                modify_user_config(current_user, head_portrait=filename)  # 修改用户配置信息
        nickname = request.form['nickname'].strip()
        signature = request.form['signature'].strip()
        new_nickname = nickname if nickname else current_user.nickname
        new_signature = signature if signature else current_user.signature

        from ... import db
        u = User.query.filter_by(id=current_user.id).first()
        u.nickname = new_nickname
        u.signature = new_signature
        db.session.commit()

        return redirect(url_for('u.home'))

    return render_template('u/profile.html')








