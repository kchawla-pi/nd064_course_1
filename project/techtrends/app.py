from pathlib import Path

from flask import Flask, make_response, render_template, request, url_for, redirect, flash

from project.techtrends.src.functionality import (count_posts, get_post,
                                                  )
from project.techtrends.src.connection import ConnectionManager


# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
connection_mgr = ConnectionManager(db_path=Path('database.db'))


@app.route('/')
def index():
    """
    Define the main route of the web application
    """
    global connection_mgr
    with connection_mgr.connect() as connection:
        posts = connection.execute('SELECT * FROM posts').fetchall()
    return render_template('index.html', posts=posts)


@app.route('/<int:post_id>')
def post(post_id):
    """
    Define how each individual article is rendered
    If the post ID is not found a 404 page is shown

    :param post_id:
    :return:
    """
    global connection_mgr
    post = get_post(connection_mgr, post_id)
    return render_template('post.html', post=post) if post else render_template(
        '404.html'
        ), 404


@app.route('/about')
def about():
    """
    Define the About Us page
    :return:
    """
    return render_template('about.html')


@app.route('/create', methods=('GET', 'POST'))
def create():
    """
    Define the post creation functionality
    :return:
    """
    global connection_mgr
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            with connection_mgr.connect() as connection:
                connection.execute(
                    'INSERT INTO posts (title, content) VALUES (?, ?)',
                    (title, content)
                    )
                connection.commit()
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/healthz', methods=('GET',))
def get_health():
    return make_response({"result": "OK - health"}, 200)


@app.route('/metrics', methods=('GET',))
def get_metrics():
    global connection_mgr
    return make_response({
        "post_count": count_posts(connection_mgr),
        "db_connection_count": connection_mgr._count,
        },
        200,
        )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3111)
