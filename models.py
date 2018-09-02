from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager
from datetime import datetime
# flask-login 统一管理id值，每个model的主键id自动赋值并管理


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')  # 其中role只是个名字，用于定义User时的一个变量

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model, UserMixin):
    '''用户登录信息表'''
    __tablename__ = 'LoginUser'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), unique=True)  # 登录用户名
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # 角色
    password_hash = db.Column(db.String(128))  # 密码的hash

    # 用户个人信息
    nickname = db.Column(db.String(32), default='小白')  # 昵称
    signature = db.Column(db.String(256))  # 个性签名

    articles = db.relationship('Article', backref='user', lazy='dynamic')  # 用户的文章

    def __repr__(self):
        return f'UserName: {self.username}'

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)  # 将密文生成hash

    def verify_password(self, password):
        '''检验用户名'''
        return check_password_hash(self.password_hash, password)


# 对于每篇文章采用一个单独的文件夹保存其 .md, .png, .jpg等，文章名即为文件名，文件夹为id
# 文件夹位置：/static/u/<user_id>/<articleID>/
class Article(db.Model):
    '''用户的创作'''
    __tablename__ = 'Article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 文章id
    user_id = db.Column(db.Integer, db.ForeignKey('LoginUser.id'), nullable=False)  # 作者
    title = db.Column(db.String(128))  # 文章标题/文章名
    synopsis = db.Column(db.String(1024))  # 文章简介
    publish_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 文章创作日期
    classification = db.Column(db.String(32))  # 文章分类 -- 唯一型tag

    # 文章保密级:
    # secret(默认，仅自己可见)
    # public(匿名可见)
    # ... (未定义)
    secrecy = db.Column(db.String(16), default='secret')

    # 储存
    raw_filename = db.Column(db.String(256))  # 文件上传前文件名
    file_name = db.Column(db.String(256))  # 系统储存文件名


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == "__main__":
    pass



