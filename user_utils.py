import sqlServer

con = sqlServer.connect()
cur = con.cursor() #required to execute sql query

def getAllUsers():
    sql = "select * from users"
    cur.execute(sql)

    json = dict()

    rows = cur.fetchall()
    for r in rows:
        userID = r[0]
        name = r[1]
        email = r[2]
        password = r[3]
        json[userID] = {'name': name, 'email': email, 'password': password}
    return json

def isUserExist(info:str, password:str):
    # info is email or username
    sql = f"select * from users where (name = '{info}' or email = '{info}') and password = '{password}'"
    cur.execute(sql)
    return bool(cur.fetchone()) 
#fetchone return a tuple consist of datas in 1 row of table from sql
#if tuple is empty, it is considered false. Same thing to list, set, dict, string    

def insertUser(name, email, password):
    sql = f"insert into users (name, email, password) values ('{name}', '{email}', '{password}')"
    cur.execute(sql)

if __name__ == "__main__":
    i =  isUserExist("John ", "hashed_password")
    print(i) # >>> false