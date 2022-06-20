import logging
from flask import Blueprint, render_template, request, send_from_directory
from utils import get_posts_by_contains_text, load_posts
from json import JSONDecodeError

logger = logging.getLogger(__name__)
main_blueprint = Blueprint('main_blueprint', __name__, template_folder='templates')


@main_blueprint.route("/uploads/<path:path>")
def static_dir(path):
    return send_from_directory("uploads", path)


@main_blueprint.route('/')
def index_page():
    return render_template('index.html')


@main_blueprint.route('/search/')
def search_page():
    search_tag = request.args.get('s', '')
    try:
        posts = get_posts_by_contains_text(load_posts(), search_tag)

    except FileNotFoundError as e:
        logger.error(f'Ошибка загрузки файла: {e}')
        title = 'Ошибка загрузки файла'
        text = 'Файл не найден'
        return render_template('error_page.html', title=title, text=text), 404

    except JSONDecodeError as e:
        logger.error(f'Ошибка загрузки файла: {e}')
        title = 'Ошибка загрузки файла'
        text = 'Не корректный JSON файл'
        return render_template('error_page.html', title=title, text=text), 404

    logger.info(f'Выполнен поиск по фразе "{search_tag}"')
    return render_template('post_list.html', search=search_tag, posts=posts)
