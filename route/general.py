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
    ''' 删除文章 '''
    article_id = request.args.get('article')
    # 未传入参数article
    if not article_id:
        return "failed"
    from ..models import Article
    essay = Article.query.filter_by(id=article_id).first()  # 找到对应id的文章
    # 找不到对应文章
    if not essay:
        return "article not found"
    if current_user.id == essay.userid:  # 若文章作者id等于当前用户id
        from db import db
        db.session.delete(essay)
        db.session.commit()
    return "success"


@mod.route('/article/<article_id>')
@login_required
def reading(article_id):
    from ..models import Article
    essay = Article.query.filter_by(id=article_id).first()  # 找到对应id的文章
    if not essay or current_user.id != essay.userid:
        flash('文章不存在或权限错误')
        return redirect(url_for('index.index'))
    # 文件目录:  static/u/<userid>/filename
    with open(f'static/u/{current_user.id}/{essay.file_name}', encoding='utf8') as f:
        r = my_md2html(f.read())
    return render_template('essay.html', content=r, title=essay.title)


def my_md2html(md):
    import markdown
    import bleach

    allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i',
                    'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'h4', 'h5',
                    'p', 'table', 'thead', 'tbody', 'td', 'tr', 'th', 'hr'
                    ]
    # 初步生成html
    t = markdown.markdown(md, output_format='html',
                          extensions=[
                              # 'urlize',
                              'fenced_code',
                              'codehilite(css_class=highlight)',
                              'toc',
                              'tables',
                              'sane_lists',
                          ])
    # 净化html
    html = bleach.linkify(bleach.clean(t, tags=allowed_tags, strip=True))

    return html


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




