import sqlite3

DB_NAME = 'users.db'
USER_TABLE = "users"

g_Sqlte3_Connection = None

def init_db():
    g_Sqlte3_Connection = sqlite3.connect(DB_NAME)
    if g_Sqlte3_Connection:
        g_Sqlte3_Connection.execute(f'''
            CREATE TABLE IF NOT EXISTS {USER_TABLE} (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                usertype INTEGER NOT NULL
            );
        ''')

############################################################################################
#	Add new user to the database.
#	Return True if successed, False if username is existed.
############################################################################################
def AddUser(username, password, usertype):
    try:
        if g_Sqlte3_Connection:
            g_Sqlte3_Connection.execute(
                f'INSERT INTO {USER_TABLE} (username, password, usertype) VALUES (?, ?, ?);',
                (username, password, usertype)
            )
        return True
    except sqlite3.IntegrityError:
        return False  # username đã có trong DB
    
############################################################################################
#    Remove user by username.
#    Return True if remove successed (rowcount > 0), False if the user is not found.
############################################################################################
def RemoveUser(username):
    """
    Remove user by username.
    Return True if remove successed (rowcount > 0), False if the user is not found.
    """
    if g_Sqlte3_Connection:
        g_Sqlte3_Connection.execute(
            f'DELETE FROM {USER_TABLE} WHERE username = ?;',
            (username,)
        )
        return cursor.rowcount > 0

############################################################################################
#    return dictionary contains the information of user, other returns None.
#    Structure: {'username': ..., 'password': ..., 'usertype': ...}
############################################################################################  
def GetUser(username):
    if g_Sqlte3_Connection:
        g_Sqlte3_Connection.row_factory = sqlite3.Row
        cursor = g_Sqlte3_Connection.execute(
            f'SELECT username, password, usertype FROM {USER_TABLE} WHERE username = ?;',
            (username,)
        )
        row = cursor.fetchone()
    return dict(row) if row else None

############################################################################################
#    return dictionary contains the information of user, other returns None.
#    Structure: {'username': ..., 'password': ..., 'usertype': ...}
############################################################################################  
def GetAllUsers():
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute('SELECT username, password, usertype FROM users;')
        rows = cursor.fetchall()
    return [dict(row) for row in rows]
