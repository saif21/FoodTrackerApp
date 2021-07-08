import mysql.connector as mysql

config = {
    'user': 'root',
    'host': 'localhost',
    'passwd': 'saif1721',
    'database': 'projectOne'
}

db = mysql.connect(**config)
cursor = db.cursor(dictionary=True, buffered=True)
