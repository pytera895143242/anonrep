import sqlite3

db = sqlite3.connect('server.db')
sql = db.cursor()

def reg_bd():
    sql.execute(""" CREATE TABLE IF NOT EXISTS queue (
            chat_id,
            gender_find,
            my_gender
            ) """)
    db.commit()

    sql.execute(""" CREATE TABLE IF NOT EXISTS sessions (
                id,
                chat_one,
                chat_two
                ) """)
    db.commit()

    sql.execute(""" CREATE TABLE IF NOT EXISTS users (
                    chat_id,
                    gender,
                    first_name,
                    ref
                    ) """)
    db.commit()

    sql.execute(""" CREATE TABLE IF NOT EXISTS trafik(
                chanel,
                parametr,
                chat_channel
                ) """)
    db.commit()
    sql.execute(f"SELECT chanel FROM trafik WHERE chanel = 'channel1'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO trafik VALUES (?,?,?)", ('channel1', 'https://t.me/+Q4OLKIg_HX03Mzdi', -1001401463447))
        sql.execute(f"INSERT INTO trafik VALUES (?,?,?)", ('channel2', 'https://yandex.ru/news/?utm_source=main_stripe_big', -111))
        sql.execute(f"INSERT INTO trafik VALUES (?,?,?)", ('channel3', 'https://www.youtube.com/', -111))
        db.commit()

def cheak_chat_id():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    i1 = sql.execute(f"SELECT chat_channel FROM trafik WHERE chanel = 'channel1'").fetchone()[0]
    i2 = sql.execute(f"SELECT chat_channel FROM trafik WHERE chanel = 'channel2'").fetchone()[0]
    i3 = sql.execute(f"SELECT chat_channel FROM trafik WHERE chanel = 'channel3'").fetchone()[0]
    return i1,i2,i3

def info_members():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f'SELECT COUNT(*) FROM users').fetchone()[0]
    return a

def cheak_traf():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    c1 = sql.execute(f"SELECT parametr FROM trafik WHERE chanel = 'channel1'").fetchone()[0]
    c2 = sql.execute(f"SELECT parametr FROM trafik WHERE chanel = 'channel2'").fetchone()[0]
    c3 = sql.execute(f"SELECT parametr FROM trafik WHERE chanel = 'channel3'").fetchone()[0]

    list = [c1,c2,c3]
    return list

def obnovatrafika1(link_one,id_channel1):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"UPDATE trafik SET parametr= '{link_one}' WHERE chanel = 'channel1'")
    sql.execute(f"UPDATE trafik SET chat_channel= '{id_channel1}' WHERE chanel = 'channel1'")
    db.commit()

def obnovatrafika2(link_one,id_channel1):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"UPDATE trafik SET parametr= '{link_one}' WHERE chanel = 'channel2'")
    sql.execute(f"UPDATE trafik SET chat_channel= '{id_channel1}' WHERE chanel = 'channel2'")
    db.commit()


def obnovatrafika3(link_one,id_channel1):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"UPDATE trafik SET parametr= '{link_one}' WHERE chanel = 'channel3'")
    sql.execute(f"UPDATE trafik SET chat_channel= '{id_channel1}' WHERE chanel = 'channel3'")
    db.commit()


def reg_in_users(chat_id,first_name,ref):
    sql.execute(f"SELECT chat_id FROM users WHERE chat_id ='{chat_id}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO users VALUES (?,?,?,?)", (str(chat_id),'wait',first_name,str(ref)))
        db.commit()

def get_my_gender(chat_id):
    my_gender = sql.execute(f"SELECT gender FROM users WHERE chat_id = '{chat_id}'").fetchone()
    return my_gender[0]


def reg_gender(chat_id, gender, first_name):
    sql.execute(f"SELECT chat_id FROM users WHERE chat_id ='{chat_id}' and gender = 'wait'")
    if sql.fetchone() is not None:
        sql.execute(f"UPDATE users SET gender = '{gender}' WHERE chat_id ='{chat_id}' and gender = 'wait'")
        db.commit()
        return '1'

    else:
        sql.execute(f"SELECT chat_id FROM users WHERE chat_id ='{chat_id}' and (gender = 'man' or gender = 'woman')")
        if sql.fetchone() is None:
            """Не нашел кому менять пол (создаю запись)"""
            sql.execute(f"INSERT INTO users VALUES (?,?,?,?)", (str(chat_id), gender, first_name, '1'))
            db.commit()
            return '1'
        else:
            return '0'


def find_man(chat_id):  # Поиск парня
    my_gender = get_my_gender(chat_id = chat_id)
    a = sql.execute(f"SELECT * FROM queue WHERE my_gender = 'man' and (gender_find = '{my_gender}' or gender_find = 'any')").fetchone()
    if a is None:
        q = 'Поставлен в очередь'
        sql.execute(f"SELECT chat_id FROM queue WHERE chat_id ='{chat_id}'")
        if sql.fetchone() is None:
            sql.execute(f"INSERT INTO queue VALUES (?,?,?)", (str(chat_id),'man',my_gender))
            db.commit()
        return '1'
    else:
        if (a[0]) != str(chat_id): #ПРОВЕРКА ЧТОБЫ ЧЕЛОВЕК НЕ ПОДКЛЮЧИЛСЯ САМ К СЕБЕ
            q = f'Соединен с {a[0]} '
            reg_session(chat_one= chat_id, chat_two = a[0])
            return [a[0],'True']
    return '1'


def find_woman(chat_id):  # Поиск Девушки
    my_gender = get_my_gender(chat_id = chat_id)
    a = sql.execute(f"SELECT * FROM queue WHERE my_gender = 'woman' and (gender_find = '{my_gender}' or gender_find = 'any')").fetchone()
    if a is None:
        q = 'Поставлен в очередь'
        sql.execute(f"SELECT chat_id FROM queue WHERE chat_id ='{chat_id}'")
        if sql.fetchone() is None:
            sql.execute(f"INSERT INTO queue VALUES (?,?,?)", (str(chat_id),'woman',my_gender))
            db.commit()
    else:
        if (a[0]) != str(chat_id):  # ПРОВЕРКА ЧТОБЫ ЧЕЛОВЕК НЕ ПОДКЛЮЧИЛСЯ САМ К СЕБЕ
            reg_session(chat_one=chat_id, chat_two=a[0])
            q = f'Соединен с {a[0]}'
            db.close()
            return [a[0],'True']
    return '1'

def find_any(chat_id):  # Рандомный поиск
    my_gender = get_my_gender(chat_id = chat_id)

    a = sql.execute(f"SELECT * FROM queue WHERE gender_find = '{my_gender}' or gender_find = 'any'").fetchone()
    if a is None:
        q = 'Поставлен в очередь'
        sql.execute(f"SELECT chat_id FROM queue WHERE chat_id ='{chat_id}'")
        if sql.fetchone() is None:
            sql.execute(f"INSERT INTO queue VALUES (?,?,?)", (str(chat_id), 'any' ,my_gender))
            db.commit()
    else:
        if (a[0]) != str(chat_id):  # ПРОВЕРКА ЧТОБЫ ЧЕЛОВЕК НЕ ПОДКЛЮЧИЛСЯ САМ К СЕБЕ
            reg_session(chat_one = chat_id, chat_two = a[0])
            q = f'Соединен с {a[0]}'
            return [a[0],'True']
    return '1'



def del_in_queue(chat_id): #Удаляем с очереди
    sql.execute("DELETE FROM queue WHERE chat_id = ?", (str(chat_id),))
    db.commit()


def reg_session(chat_one,chat_two): #Регистрация сессии
    #Теперь чистим очередь
    print(f'Чистка {chat_two} {chat_one}')

    sql.execute("DELETE FROM queue WHERE chat_id = ? ", (str(chat_one),))

    sql.execute("DELETE FROM queue WHERE chat_id = ? ", (str(chat_two),))

    sql.execute(f"SELECT chat_one FROM sessions WHERE chat_one = '{chat_one}' or chat_one = '{chat_two}'")
    if sql.fetchone() is None: #Если никто не учавствует в другом диалоге, то созадем сессию
        sql.execute(f"INSERT INTO sessions VALUES (?,?,?)", (0,str(chat_one),str(chat_two)))
        db.commit()



def del_session(chat_id): # Удаление сессии
    another_id = cheack_another_chat_id(chat_id=chat_id)

    try:
        print('отключаем')
        sql.execute("DELETE FROM sessions WHERE chat_one = ? ", (str(chat_id),))
    except: pass
    try:
        print('отключаем 2')
        sql.execute("DELETE FROM sessions WHERE chat_two = ? ", (str(chat_id),))
    except: pass

    db.commit()
    return another_id


def cheack_another_chat_id(chat_id):
    try:
        chats_all = (sql.execute(f"SELECT * FROM sessions WHERE chat_one = '{chat_id}' or chat_two = '{chat_id}'").fetchall())[0]
        if chats_all[1] == str(chat_id):
            return chats_all[2]
        else:
            return chats_all[1]
    except:
        return '1'


def cheack_session(chat_id):
    try:
        chats_all = (sql.execute(f"SELECT * FROM sessions WHERE chat_one = '{chat_id}' or chat_two = '{chat_id}'").fetchall())[0]
        return 0
    except:
        return '1'


