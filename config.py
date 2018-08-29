import os
# base_dir = os.path.abspath(os.path.dirname(__file__))  # 当前文件路径
base_dir = os.getcwd()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    # FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(base_dir, 'data.sqlite')  # 数据库位置
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # 自动追踪修改（需要额外内存）
    ALLOWED_EXTENSIONS = {'txt', 'md', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

    @staticmethod
    def init_app(app):
        pass
