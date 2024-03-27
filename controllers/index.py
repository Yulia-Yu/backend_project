from app import app

from flask import render_template, request, session
#import sqlite3
from utils import get_db_connection
from models.index_model_1 import get_reader, get_book_reader, borrow_book,  get_new_reader#, return_book
@app.route('/', methods=['get'])
def index():
    conn = get_db_connection()

    # нажата кнопка Найти
    if request.values.get('reader'):
        reader_id = int(request.values.get('reader'))
        session['reader_id'] = reader_id

    elif request.values.get('return'):
        print('bbb')
        reader_book_id = int(request.values.get('return'))
        #return_book(conn, reader_book_id)

    # нажата кнопка Добавить со страницы Новый читатель (Переделать на авторизацию)
    elif request.values.get('new_reader'):
        new_reader = request.values.get('new_reader')
        psw_reader = request.values.get('psw_reader')
        reader_now = get_new_reader(conn, new_reader, psw_reader)
        print('reader_now ' + str(reader_now))
        session['reader_id'] = reader_now
        print('session '+str(session['reader_id']))
    # нажата кнопка Взять со страницы Поиск
    #(взять в комментарии, пока не реализована страница Поиск)  Переделать на забронированно
    elif request.values.get('book'):
        print('aaa ' + str(session['reader_id']))
        book_id = int(request.values.get('book'))
        borrow_book(conn, book_id, session['reader_id'])
    # нажата кнопка Не брать книгу со страницы Поиск
    elif request.values.get('noselect'):
        a = 1
    # вошли первый раз
    else:
        session['reader_id'] = 8

    df_reader = get_reader(conn)
    df_book_reader = get_book_reader(conn, session['reader_id'])

    print(session['reader_id'])


    # выводим форму
    html = render_template(
    'index.html',
        reader_id = session['reader_id'],
        combo_box = df_reader,
        book_reader = df_book_reader,
        len = len
    )
    return html