import logging

from project.techtrends.src.connection import DBConnectionManager


LOGGER = logging.getLogger(__name__)


def get_post(connection_manager: DBConnectionManager, post_id):
    """
    Function to get a post using its ID
    """
    with connection_manager.connect() as connection:
        post = connection.execute('SELECT * FROM posts WHERE id = ?',
                                  (post_id,)
                                  ).fetchone()
    if post:
        LOGGER.debug('Article found: %s', post["title"])
    else:
        LOGGER.debug("No article with ID %s found.", post_id)
    return post

def count_posts(connection_manager: DBConnectionManager) -> int:
    with connection_manager.connect() as connection:
        return connection.execute('SELECT COUNT(*) FROM posts').fetchone()[0]


def write_post(db_connection, title, content):
    with db_connection.connect() as connection:
        connection.execute(
            'INSERT INTO posts (title, content) VALUES (?, ?)',
            (title, content)
            )
        connection.commit()
        LOGGER.debug("Article created: %s", title)
