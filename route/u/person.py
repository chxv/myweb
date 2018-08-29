from flask import Blueprint, redirect, render_template, url_for, flash, request, current_app
from flask_login import login_required, current_user
# from werkzeug.utils import secure_filename
# import os
# from app import app

mod = Blueprint('u', __name__, url_prefix='/u')


@mod.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    from ...models import Article
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
        if not allowed_file(file.filename):
            flash('File type error!')
            return redirect(request.url)
        if file:

            # 保存文件
            import random
            import datetime
            filename = str(random.randrange(0, 1024, 1)) + datetime.datetime.now().strftime('-%y%m%d%H%M%S%f') + \
                       '.' + file.filename.rsplit('.', 1)[1]  # 确保文件安全以及避免同名文件
            upload_folder = f'static/u/{current_user.id}/'   # static/u/<userid>/filename
            file.save(upload_folder + filename)
            # 保存文件信息到数据库
            new_essay = Article(userid=current_user.id, title=request.form['title'],
                                synopsis=request.form['about'], classification=request.form['classification'],
                                raw_filename=file.filename, file_name=filename)
            from db import db
            db.session.add(new_essay)
            db.session.commit()
            return redirect(url_for('u.home'))

    articles = Article.query.filter_by(userid=current_user.id).all()

    info = {
        'head_portrait': 'tou.jpg',  # 头像位置
        'userid': current_user.id,  # 用户的id
        'username': current_user.username,  # 用户名
        'articles': articles  # 文章列表
    }
    # 用户文件夹 /static/u/<userid>/
    return render_template('u/home.html', info=info)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']




