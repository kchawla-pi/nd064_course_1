import logging
from pathlib import Path

from flask import Flask, make_response, render_template, request, url_for, redirect, flash

from project.techtrends.src.functionality import (
    count_posts,
    get_post, write_post,
    )
from project.techtrends.src.connection import DBConnectionManager

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
DB_CONNECTION = DBConnectionManager(db_path=Path('database.db'))


@app.route('/')
def index():
    """
    Define the main route of the web application
    """
    with DB_CONNECTION.connect() as connection:
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
    post = get_post(DB_CONNECTION, post_id)
    if post:
        return render_template('post.html', post=post), 200
    else:
        return render_template('404.html'), 404


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
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Title is required!')
        else:
            write_post(DB_CONNECTION, title, content)
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/healthz', methods=('GET',))
def health():
    return make_response({"result": "OK - health"}, 200)


@app.route('/metrics', methods=('GET',))
def metrics():
    return make_response(
        {
            "post_count": count_posts(DB_CONNECTION),
            "db_connection_count": DB_CONNECTION.count,
            },
        200,
        )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3111)
