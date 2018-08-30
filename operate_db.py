# This file is created for development
# Use current file to insert, modify, delete all of data which I need
# Just for development


def insert_data(db):
    '''insert some data for use'''
    from .models import User, Role, Article
    # 角色
    Anonymous_role = Role(name='Anonymous')  # 访客
    Ordinary_role = Role(name='Ordinary')  # 普通用户
    Admin_role = Role(name='Admin')  # 管理员

    # 用户
    Tony = User(username='Tony', role=Admin_role, password='123')
    zz = User(username='Guest', role=Anonymous_role, password='123')
    Bob = User(username='Bob', role=Ordinary_role, password='123')

    # 文章

    # 将记录添加到会话
    db.session.add(Admin_role)
    db.session.add(Anonymous_role)
    db.session.add(Ordinary_role)

    db.session.add(Tony)
    db.session.add(zz)
    db.session.add(Bob)

    # db.session.add(Essay)

    # 提交
    db.session.commit()


def remove_data(db):
    '''remove all of data'''
    pass


def indite_article(db, user, title, classification=''):
    pass




