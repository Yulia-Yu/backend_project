import pandas as pd

def get_reader(conn):
    return pd.read_sql(
        '''
        SELECT id, lastname ||' '|| firstname ||' '|| fathername AS reader_name
        FROM USERS 
        WHERE rool = 3;
        ''', conn)


def get_book_reader(conn, reader_id):
    return pd.read_sql(
        '''
        SELECT Book.name AS Название, Genre.name_genre AS Жанр, bool_issuance.Date AS Дата_выдачи, bool_issuance.Date_V AS Дата_сдачи 
        FROM bool_issuance
        INNER JOIN Book ON Book.id = bool_issuance.id_book
        INNER JOIN Genre ON Genre.id = Book.id_genre
        INNER JOIN Users ON Users.id = bool_issuance.id_reader
        WHERE Users.id = :id
        ORDER BY Book.name
        ''', conn, params={"id": reader_id})


# для обработки данных о взятой книге
def borrow_book(conn, book_id, reader_id):
    cur = conn.cursor()
    id_list = cur.execute('''SELECT MAX(id) FROM bool_issuance; ''').fetchall()
    id_r_b = id_list[0][0] + 1
    cur.execute('''
            insert into bool_issuance (id, id_book, id_reader, id_bibl, Date)
            values (:id_r_b, :book_id, :reader_id, 5, DATE('now'))
        ''', {'id_r_b': id_r_b,'book_id': book_id, 'reader_id': reader_id})
    conn.commit()

    cur.execute('''
            UPDATE Book
            SET number_of_copies = number_of_copies - 1
            WHERE id = :book_id
        ''', {'book_id': book_id})
    conn.commit()

    return True

def get_new_reader(conn, new_reader, psw_reader):
    cur = conn.cursor()
    print("new_reader")
    # добавить нового читателя в базу
    cur.execute(
        ''' 
           SELECT id, lastname ||' '|| firstname ||' '|| fathername
            FROM USERS
            WHERE :new_reader == lastname ||' '|| firstname ||' '|| fathername AND id == :psw_reader; 
        ''',
        {"new_reader": new_reader, "psw_reader": psw_reader}
    )
    conn.commit()
    # Получение результата запроса
    reader = cur.fetchone()
    print('rader' + str(reader))
    # Если читатель найден, вернуть его ID
    if reader:
        return reader[0]
    else:
        return None

