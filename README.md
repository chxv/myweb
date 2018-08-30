### My web
* 小型网站
* 供学习交流使用

#### Usage
* 构建数据库

> 若项目文件夹名为App，进入项目执行: 
```shell
    $ pip install -r requirements.txt
    $ python -m flask shell
    ...
    >>> from App.db import db
    >>> from App.operate_db import insert_data
    >>> db.drop_all()
    >>> db.create_all()
    >>> insert_data(db)
    >>> exit()
```
> 进入shell后创建数据库，可适当插入数据。
> 通过修改operate_db修改数据的角色与用户等信息

* 运行
> 执行以下代码

```shell
    flask run --host 0.0.0.0 --port 80
```

