import psycopg2 as psy
from config.bot_config import load_database_config
from random import choice


config = load_database_config()
db = psy.connect(user=config.user,
                 password=config.password, host='localhost', port='5432')


async def db_start():
    cur = db.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
        user_id text PRIMARY KEY,
        name text,
        sex text,
        age integer,
        city text,
        languages text[],
        description text,
        photo text,
        watched_users text[]
        );
        ''')
    db.commit()
    cur.close()


async def check_user_in_database(user_id: int) -> tuple:
    cur = db.cursor()
    cur.execute(f'''
        SELECT 1 
        FROM users 
        WHERE user_id = '{user_id}';
        ''')
    user = cur.fetchone()
    cur.close()
    return user


async def create_profile(user_id: int, data: dict) -> None:
    cur = db.cursor()
    cur.execute(f'''
        INSERT INTO users(user_id, name, sex, age, city, languages, description, photo, watched_users)
        VALUES({user_id}, '{data['name']}', '{data['sex']}', {data['age']}, '{data['city']}',
                   ARRAY{data['languages']}, '{data['description']}', '{data['photo']}', ARRAY{["default"]}::text[]);
    ''')
    db.commit()
    cur.close()


async def delete_profile(user_id: int):
    cur = db.cursor()
    cur.execute(f'''
        DELETE 
        FROM USERS 
        WHERE user_id='{user_id}';
        ''')
    db.commit()
    cur.close()


async def get_profile(user_id: int) -> tuple:
    cur = db.cursor()
    cur.execute(f'''
        SELECT user_id, name, sex, age, city, languages, description, photo 
        FROM USERS 
        WHERE user_id='{user_id}';
        ''')
    profile = cur.fetchone()
    cur.close()
    return profile


async def edit_profile(user_id: int | str,
                       edit_parametr: str,
                       edit_value: str | int | list,
                       remove: bool = False) -> None:
    cur = db.cursor()
    if isinstance(edit_value, list):
        cur.execute(f'''
            UPDATE users 
            SET {edit_parametr} = ARRAY{edit_value} 
            WHERE user_id = '{user_id}';
            ''')
    elif isinstance(edit_value, int):
        cur.execute(f'''
            UPDATE users 
            SET {edit_parametr} = {edit_value} 
            WHERE user_id = '{user_id}';
            ''')
    elif edit_parametr == 'watched_users' and not remove:
        cur.execute(f'''
            UPDATE users 
            SET {edit_parametr} = ARRAY_APPEND({edit_parametr}, '{edit_value}')
            WHERE user_id = '{user_id}';
            ''')
    elif remove:
        cur.execute(f'''
            UPDATE users 
            SET {edit_parametr} = ARRAY_REMOVE({edit_parametr}, '{edit_value}')
            WHERE user_id != '{user_id}';
            ''')
    else:
        cur.execute(f'''
            UPDATE users 
            SET {edit_parametr} = '{edit_value}' 
            WHERE user_id = '{user_id}';
            ''')
    db.commit()
    cur.close()


async def search_profile(user_id: int) -> list | bool:
    cur = db.cursor()
    cur.execute(f'''
            SELECT languages 
            FROM USERS 
            WHERE user_id='{user_id}';
        ''')
    languages = cur.fetchone()[0]
    cur.execute(f'''
        SELECT user_id, languages 
        FROM users 
        WHERE user_id != '{user_id}' 
        AND (
            user_id != ALL (
            ARRAY(
                SELECT watched_users 
                FROM users 
                WHERE user_id = '{user_id}')
                )
            )
    ''')
    get_profiles = cur.fetchall()
    cur.close()
    if get_profiles:
        profile = choice([i for i in get_profiles if any(lang in i[-1] for lang in languages)])
        res = await get_profile(profile[0])
        return list(res)
    else:
        return False
