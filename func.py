def allowed_file(filename):
    from flask import current_app
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def my_md2html(md):
    '''markdown to html'''
    import markdown
    import bleach

    allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i',
                    'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'h4', 'h5',
                    'p', 'table', 'thead', 'tbody', 'td', 'tr', 'th', 'hr', 'img'
                    ]
    allowed_attrs = {'*': ['class', 'id', 'align'],
                     'a': ['href'],
                     'img': ['src', 'alt']}
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
    html = bleach.linkify(bleach.clean(t, tags=allowed_tags, attributes=allowed_attrs, strip=True))

    return html


def get_article(essay):
    '''获取用户文章（可以是其他用户的文章）'''
    with open(f'static/u/{essay.user_id}/{essay.file_name}', encoding='utf8') as f:
        content = my_md2html(f.read())
    return content


def get_user_config(config_file):
    with open(config_file, encoding='utf8') as f:
        confs = f.readlines()
    r = dict()
    for conf in confs:
        key, value = conf.split('=')
        r[key] = value
    return r



