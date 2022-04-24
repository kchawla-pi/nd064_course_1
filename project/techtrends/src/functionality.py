from project.techtrends.src.connection import DBConnectionManager, yield_db_connection


def get_post(connection_manager: DBConnectionManager, post_id):
    """
    Function to get a post using its ID
    """
    with connection_manager.connect() as connection:
        return connection.execute('SELECT * FROM posts WHERE id = ?',
                                  (post_id,)
                                  ).fetchone()


def count_posts(connection_manager: DBConnectionManager) -> int:
    with connection_manager.connect() as connection:
        return connection.execute('SELECT COUNT(*) FROM posts').fetchone()[0]


def make_post(db_connection, title, content):
    with db_connection.connect() as connection:
        connection.execute(
            'INSERT INTO posts (title, content) VALUES (?, ?)',
            (title, content)
            )
        connection.commit()
