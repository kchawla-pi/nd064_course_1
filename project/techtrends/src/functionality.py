from project.techtrends.src.connection import ConnectionManager, yield_db_connection


def get_post(connection_manager: ConnectionManager, post_id):
    """
    Function to get a post using its ID
    """
    with connection_manager.connect() as connection:
        post = connection.execute('SELECT * FROM posts WHERE id = ?',
                                  (post_id,)
                                  ).fetchone()
    return post


def count_posts(connection_manager: ConnectionManager) -> int:
    with connection_manager.connect() as connection:
        return connection.execute('SELECT COUNT(*) FROM posts').fetchone()[0]
