from flask import Blueprint, redirect, render_template, url_for, request, flash, g
from flask_login import current_user, login_required

mod = Blueprint('index', __name__)  # 根目录


@mod.route('/')
def index():
    return render_template('index.html')


@mod.route('/index')
def index2():
    return redirect(url_for('index.index'))  # 第一个index是命名空间，是mod的名字（第一个参数），第二个表示端点


@mod.route('/home')
def home2():
    return redirect(url_for('u.home'))


@mod.route('/search')
def search():
    ''' 搜索 '''
    q = request.args.get('q')

    return render_template('search.html', q=q)


@mod.route('/explore')
def explore():
    return render_template('explore.html')


@mod.route('/d')
@login_required
def delete():
    ''' 删除文章 [ 使用get ]'''
    article_id = request.args.get('article')
    # 未传入参数article
    if not article_id:
        return "failed", 403
    from ..models import Article
    essay = Article.query.filter_by(id=article_id).first()  # 找到对应id的文章
    # 找不到对应文章
    if not essay:
        return "failed", 403
    if current_user.id == essay.user_id:  # 若文章作者id等于当前用户id
        from .. import db
        db.session.delete(essay)
        db.session.commit()
    return "success"


@mod.route('/changeArticlePermission', methods=['POST'])
@login_required
def changeArticlePermission():
    '''改变文章的状态 [ 使用post ]'''
    from ..models import Article
    from .. import db
    # 检查http方法
    if request.method == 'POST':
        # 检查参数
        if 'article_id' in request.form and 'secrecy' in request.form:
            article_id, secrecy = request.form['article_id'], request.form['secrecy']
            essay = Article.query.filter_by(id=article_id).first()
            # 检查文章是否存在
            if essay:
                # 检查用户权限
                if current_user.id == essay.user_id:
                    essay.secrecy = secrecy
                    db.session.commit()
                    return 'success'
    return 'Forbidden', 403


def cannot_get_article():
    '''当无法获取文章时:'''
    flash('文章不存在或权限错误')
    return redirect(url_for('index.index'))


@mod.route('/article/<article_id>')
def reading(article_id):
    from ..models import Article
    from ..func import get_article
    essay = Article.query.filter_by(id=article_id).first()  # 找到对应id的文章
    # 文章不存在
    if not essay:
        return cannot_get_article()
    # 文件目录:  static/u/<user_id>/filename
    if essay.secrecy == 'secret':
        if current_user.is_authenticated and (current_user.id == essay.user_id or current_user.role.name == 'Admin'):
            return render_template('essay.html', content=get_article(essay), title=essay.title)
        else:
            # 权限错误
            return cannot_get_article()
    elif essay.secrecy == 'public':
        return render_template('essay.html', content=get_article(essay), title=essay.title)





# @mod.before_request
# def before_request():
#     g.db = connect_db()
#
#
# @mod.teardown_request
# def teardown_request(exception):
#     g.db.close()
#
#
# def connect_db():
#     from flask_sqlalchemy import SQLAlchemy
#     db = SQLAlchemy()




