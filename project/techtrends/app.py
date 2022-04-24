import logging
from pathlib import Path

from flask import Flask, make_response, render_template, request, url_for, redirect, flash

from project.techtrends.src.functionality import (
    count_posts,
    get_post, make_post,
    )
from project.techtrends.src.connection import DBConnectionManager

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
db_connection_mgr = DBConnectionManager(db_path=Path('database.db'))


@app.route('/')
def index():
    """
    Define the main route of the web application
    """
    global db_connection_mgr
    with db_connection_mgr.connect() as connection:
        posts = connection.execute('SELECT * FROM posts').fetchall()
    return render_template('index.html', posts=posts)


@app.route('/<int:post_id>')
def show(post_id):
    """
    Define how each individual article is rendered
    If the post ID is not found a 404 page is shown

    :param post_id:
    :return:
    """
    global db_connection_mgr
    post = get_post(db_connection_mgr, post_id)
    if post:
        LOGGER.debug('Article found: %s', post["title"])
        page, code = render_template('post.html', post=post), 200
    else:
        LOGGER.error("No article with ID %s found.", post_id)
        page, code = render_template('404.html'), 404
    return page, code


@app.route('/about')
def about():
    """
    Define the About Us page
    :return:
    """
    LOGGER.debug("`About` page accessed")
    return render_template('about.html')


@app.route('/create', methods=('GET', 'POST'))
def create():
    """
    Define the post creation functionality
    :return:
    """
    global db_connection_mgr
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Title is required!')
        else:
            make_post(db_connection_mgr, title, content)
            LOGGER.debug("Article created: %s", title)
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/healthz', methods=('GET',))
def health():
    return make_response({"result": "OK - health"}, 200)


@app.route('/metrics', methods=('GET',))
def metrics():
    global db_connection_mgr
    return make_response({
        "post_count": count_posts(db_connection_mgr),
        "db_connection_count": db_connection_mgr.count,
        },
        200,
        )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3111)
