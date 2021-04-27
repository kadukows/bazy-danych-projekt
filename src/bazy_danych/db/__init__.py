import cx_Oracle, click, json
from flask import current_app, g, Flask
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash

from .helpers import get_lesson_instances_for_student_id

class OracleConfig:
    username = 'python_client'
    password = 'python_client'
    dsn = 'localhost'
    port = 1512
    encoding = 'UTF-8'

_pool = cx_Oracle.SessionPool(
    OracleConfig.username,
    OracleConfig.password,
    OracleConfig.dsn,
    min=12,
    max=12,
    increment=0,
    threaded=True,
    getmode=cx_Oracle.SPOOL_ATTRVAL_WAIT,
    encoding=OracleConfig.encoding
)


def get_db():
    if 'db' not in g:
        g.db = _pool.acquire()

    return g.db


def close_pool_connection(e=None):
    db = g.pop('db', None)

    if db is not None:
        _pool.release(db)


def init_db():
    raise RuntimeError("Don't call this")

    db = get_db()
    cursor = db.cursor()

    '''
    with current_app.open_resource('db/truncate.sql') as f:
        content = f.read().decode('utf8')
        for instruction in content.split(';'):
            instruction = instruction.strip()
            if instruction:
                print(instruction)
                cursor.execute(instruction)
    '''

    with current_app.open_resource('db/bogus_data.json') as f:
        bogus_data = json.loads(f.read().decode('utf8'))

    for student in bogus_data['students']:
        cursor.execute('INSERT INTO student (id, name) VALUES (:id, :name)', student)

    for teacher in bogus_data['teachers']:
        cursor.execute('INSERT INTO teacher (id, name) VALUES (:id, :name)', teacher)


    for user_account in bogus_data['user_accounts']:
        user_account["password_hash"] = generate_password_hash(user_account["password"])
        cursor.execute("INSERT INTO user_account (username, password_hash, student_id) VALUES ('foo', 'foo', 1)")
        break


    '''
    for user_account in bogus_data['user_accounts']:
        user_account["password_hash"] = generate_password_hash(user_account["password"])
        cursor.execute("""
            INSERT INTO user_account (id, username, password_hash, student_id, teacher_id)
                VALUES (:id, :username, :password_hash, :student_id, :teacher_id)
            """,
                id=user_account['id'],
                username=user_account['username'],
                password_hash=generate_password_hash(user_account['password']),
                student_id=user_account.get('student_id', None),
                teacher_id=user_account.get('teacher_id', None))
    '''


    cursor.execute('commit')




@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized db')



def init_app(app: Flask):
    app.teardown_appcontext(close_pool_connection)
    app.cli.add_command(init_db_command)
