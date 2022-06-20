import logging
from flask import Blueprint, render_template, request
from const import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from utils import add_post, save_posts, is_correct_extension

logger = logging.getLogger(__name__)
loader_blueprint = Blueprint('loader_blueprint', __name__, template_folder='templates')


@loader_blueprint.route('/post/')
def post_page():
    return render_template('post_form.html')


@loader_blueprint.route('/post/', methods=['POST'])
def add_post_page():
    picture = request.files.get('picture')
    content = request.form.get('content', '')
    if picture:
        filename = picture.filename
        img_path = f'/{UPLOAD_FOLDER}/{filename}'

        if not is_correct_extension(filename):
            logger.info(f'Неподдерживаемый тип файла: {filename}')
            title = 'Неподдерживаемый тип файла'
            text = f'Загрузите файл с расширением: {", ".join(ALLOWED_EXTENSIONS)}'
            return render_template('error_page.html', title=title, text=text), 404

        picture.save(f'.{img_path}')
        post = {'pic': img_path, 'content': content}
        save_posts(add_post(post))
        return render_template('post_uploaded.html', img_path=img_path, content=content)
    else:
        title = 'Файл не был загружен'
        text = 'Произошла ошибка при загрузке файла'
        return render_template('error_page.html', title=title, text=text), 404


@loader_blueprint.errorhandler(413)
def large_file_error_page(e):
    logger.info('Файл слишком большой')
    title = 'Файл слишком большой'
    text = 'Размер файла не должен превышать 2 Mb'
    return render_template('error_page.html', title=title, text=text), 413
