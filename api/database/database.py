import sqlite3
from database.models import Person, User
import datetime


def db_connect(fn):
    def inner(*args, **kwargs):
        con = sqlite3.connect("main_test.db")

        cursor = con.cursor()
        try:
            res = fn(*args, cur=cursor, **kwargs)
            con.commit()
        except Exception as e:
            raise e
        finally:
            con.close()
        return res
    return inner

def _build_person(data:tuple):
    _id, name, age, gender, updated_at = data
    return Person(id=_id, name=name, age=age, gender=str(gender), updated_at=updated_at)

def _build_user(data):
    _id, username, password = data
    return User(id=_id,username=username, password=password)

@db_connect
def create_tables(cur):
    cur.execute("CREATE TABLE people(id, name, age, gender, updated_at)")
    cur.execute("CREATE TABLE users(id, username, password)")

@db_connect
def get_all_people(cur):
    query = cur.execute("SELECT * FROM people")
    data = query.fetchall()
    result = []

    for tup in data:
        result.append(_build_person(tup))
    return result

@db_connect
def get_person(id:int, cur):
    query = cur.execute("SELECT * FROM people where id=%s" % id)
    res = query.fetchone()
    if res:
        return _build_person(res)

@db_connect
def create_person(data:dict, cur):
    data.update({"updated_at":datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S") })
    cur.execute(
        """ INSERT INTO people
        VALUES(%(id)s,'%(name)s',%(age)s,'%(gender)s', '%(updated_at)s')
        """ % data)
    return Person.model_validate(data)
    
@db_connect
def update_person(_id:int, data:dict, cur):
    data.update({"id":_id,"updated_at":datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S") })
    cur.execute(
        """
        UPDATE people 
        SET name='%(name)s',
            age=%(age)s,
            gender='%(gender)s',
            updated_at='%(updated_at)s'
            where id=%(id)s
        """ % data
    )
    return Person.model_validate(data)

@db_connect
def delete_person(_id:int, cur):
    cur.execute(
        """
        DELETE from people
        where id=%s""" % _id
    )

@db_connect
def create_user(data:dict, cur):
    cur.execute(
        """
        INSERT INTO users
        VALUES (%(id)s,'%(username)s', '%(password)s')
                """ % data)
    return User.model_validate(data)

@db_connect
def get_user(username:str, password:str, cur):
    q = cur.execute(
        """SELECT * from users where username='%s' AND password='%s'""" % (username, password)
    )
    res = q.fetchone()
    if res:
        return _build_user(res)
    
@db_connect
def get_users(cur):
    q = cur.execute("SELECT * FROM users")
    res = q.fetchall()
    return [_build_user(tup) for tup in res]
    