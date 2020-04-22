import sqlite3

with sqlite3.connect('sample.db') as connection:
    c = connection.cursor()
    # c.execute('DROP TABLE IF EXISTS post')
    c.execute(
        '''
            CREATE TABLE posts (
                title VARCHAR(50) NOT NULL,
                description TEXT NOT NULL
            );
        '''
    )
    c.execute('INSERT INTO posts VALUES ("Good", "I\'m good")')
    c.execute('INSERT INTO posts VALUES ("Well", "I\'m well")')
