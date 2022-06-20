import json
from const import POST_PATH, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from werkzeug.datastructures import FileStorage


def _load_json_file(filename: str) -> list[dict]:
    with open(filename, encoding='utf8') as file:
        return json.load(file)


def load_posts() -> list[dict]:
    return _load_json_file(POST_PATH)


def _save_json_file(filename: str, data: list[dict]) -> None:
    with open(filename, 'w', encoding='utf8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def save_posts(posts: list[dict]) -> None:
    _save_json_file(POST_PATH, posts)


def add_post(post: dict) -> list[dict]:
    posts = load_posts()
    posts.append(post)
    return posts


def get_posts_by_contains_text(posts: list[dict], text: str) -> list[dict]:
    search_posts = []
    for post in posts:
        if text.lower() in post["content"].lower():
            search_posts.append(post)
    return search_posts


def save_picture(picture: FileStorage) -> None:
    filename = picture.filename
    img_path = f'/{UPLOAD_FOLDER}/{filename}'
    picture.save(f'.{img_path}')


def is_correct_extension(filename: str) -> bool:
    extension = filename.split(".")[-1]
    return extension in ALLOWED_EXTENSIONS
