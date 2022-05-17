import sqlite3
import string



con = sqlite3.connect('db/database.db')
cur = con.cursor()


def createUser(uuid, username, password, f_name, l_name, email, phone):
    statement = f"""
        INSERT INTO "users" VALUES ("{username}", "{password}", "{f_name}", "{l_name}", "{email}", "{phone}")
    """
    print(statement)
    try:
        cur.execute(statement)
        return "success"
    except:
        return "failed"

def Login(username, password):
    statement = f"SELECT username from users WHERE username='{username}' AND Password = '{password}';"
    cur.execute(statement)
    if not cur.fetchone():  # An empty result evaluates to False.
        return "invalid"
    return "success"