import pandas as pd

def get_count_genre(conn):
    return pd.read_sql('''
        SELECT g.id, g.name_genre as Жанр, COUNT(b.id) AS Количество_книг
        FROM Genre g
        JOIN Book b ON g.id = b.id_genre
        GROUP BY g.id;
''', conn)


def get_count_author(conn):
    return pd.read_sql('''
        SELECT Author.id, Author.fullname as Автор, COUNT(Book.id) AS Книги_автора
        FROM Author
        LEFT JOIN Book ON Author.id = Book.id_author
        GROUP BY Author.id;
''', conn)


def get_count_publisher(conn):
    return pd.read_sql('''
        SELECT p.id, p.name_Publishing_house as Издательство, COUNT(Book.id) AS Книги_издателя
        FROM Publishing_house p
        LEFT JOIN book ON p.id = Book.id_publishing_house
        GROUP BY p.id;
''', conn)

def get_book(conn):
    return pd.read_sql('''
    SELECT b.name AS Название, GROUP_CONCAT(a.fullname) AS Автор, 
        g.name_genre AS Жанр, p.name_Publishing_house AS Издательство, 
        b.Date AS Год_издания, b.number_of_copies AS Количество, b.id AS ID_книги
    FROM Book b
        JOIN Author a ON b.id_author = a.id
        JOIN Genre g ON b.id_genre = g.id
        JOIN Publishing_house p ON b.id_publishing_house = p.id
    GROUP BY b.id;
''', conn)

def get_filter_book(conn, genre, authors, publisher):
    if not genre:
        # genre = [1, 2, 3, 4, 5, 6]
        counter = pd.read_sql(
            '''
        SELECT COUNT(*) FROM Genre
        ''', conn)
        print(counter.loc[0, "COUNT(*)"])
        for gen in range(1, counter.loc[0, "COUNT(*)"] + 1):
            genre.append(gen)

    if not authors:
        # authors = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        counter = pd.read_sql(
            '''
        SELECT COUNT(*) FROM Author
        ''', conn)
        print(counter.loc[0, "COUNT(*)"])
        for aut in range(1, counter.loc[0, "COUNT(*)"] + 1):
            authors.append(aut)

    if not publisher:
        # publisher = [1, 2, 3, 4, 5, 6, 7]
        counter = pd.read_sql(
            '''
        SELECT COUNT(*) FROM Publishing_house
        ''', conn)
        print(counter.loc[0, "COUNT(*)"])
        for pub in range(1, counter.loc[0, "COUNT(*)"] + 1):
            publisher.append(pub)
#-------------------------------------------------------------------------------------------------------------------
    query = '''
        SELECT b.name as Название, GROUP_CONCAT(a.fullname) AS Автор,
        g.name_genre as Жанр, p.name_Publishing_house as Издательство,
        b.Date as Год_публикации, b.number_of_copies AS Количество, b.id AS Книга_id

        FROM Book b
        JOIN Author a ON a.id = b.id_author
        JOIN Genre g ON b.id_genre = g.id
        JOIN Publishing_house p ON b.id_Publishing_house = p.id

        WHERE g.id IN ({})
          AND a.id IN ({})
          AND p.id IN ({})
        GROUP BY b.id;
    '''.format(','.join('?' * len(genre)), ','.join('?' * len(authors)), ','.join('?' * len(publisher)))

    params = tuple(genre + authors + publisher)
    return pd.read_sql(query, conn, params=params)
