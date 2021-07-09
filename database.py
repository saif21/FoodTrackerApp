import mysql.connector as mysql

config = {
    'user': 'root',
    'host': 'localhost',
    'passwd': '******',
    'database': '*******'
}

db = mysql.connect(**config)
cursor = db.cursor(dictionary=True, buffered=True)
