import mysql.connector as mysql

from mysql.connector import errorcode
from datetime import datetime

from database import db, cursor

DB_NAME = ['projectOne']
TABLES = {}
TABLES['log_date'] = (
    "CREATE TABLE `log_date`("
    "`id` int(10) NOT NULL AUTO_INCREMENT,"
    "`entry_date` varchar(500) NOT NULL,"
    "PRIMARY KEY(`id`)"
    ")ENGINE=InnoDB"
)
TABLES['food'] = (
    "CREATE TABLE `food`("
    "`id` int(10) NOT NULL AUTO_INCREMENT,"
    "`name` varchar(500) NOT NULL,"
    "`protein` integer NOT NULL,"
    "`carbohydrates` integer NOT NULL,"
    "`fat` integer NOT NULL,"
    "`calories` integer NOT NULL,"
    "PRIMARY KEY(`id`)"
    ")ENGINE=InnoDB"
)
TABLES['food_date'] = (
    "CREATE TABLE `food_date`("
    "`food_id` int(10) NOT NULL,"
    "`log_date_id` integer NOT NULL,"
    "PRIMARY KEY(`food_id`,`log_date_id`)"
    ")ENGINE=InnoDB"
)


def create_database():
    for name in DB_NAME:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {name}")


def create_tables():
    for name in DB_NAME:
        cursor.execute(f"USE {name}")
        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                cursor.execute(table_description)
                print(f"{table_name} is created successfully!")
            except mysql.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("table exists")
                else:
                    print(err.msg)


class Add_food:
    def addFood(self, name, protein, carbo, fat, calorie):
        self.sql = (
            "INSERT INTO food (name,protein, carbohydrates, fat, calories) VALUES(%s, %s,%s,%s,%s) ")
        cursor.execute(self.sql, (name, protein, carbo, fat, calorie,))
        db.commit()

    def getFood(self):
        self.sql = (
            "SELECT name,protein,carbohydrates,fat,calories FROM food")
        cursor.execute(self.sql,)
        result = cursor.fetchall()
        food_list = []
        for i in result:
            d = {}
            d['name'] = i['name']
            d['protein'] = i['protein']
            d['carbohydrates'] = i['carbohydrates']
            d['fat'] = i['fat']
            d['calories'] = i['calories']
            food_list.append(d)

        return food_list

    def getFoodItem(self):
        self.sql = ("SELECT id, name FROM food")
        cursor.execute(self.sql,)
        foods = cursor.fetchall()
        return foods

    def addFoodToDate(self, food, id):
        self.sql = (
            "INSERT INTO food_date(food_id,log_date_id) VALUES( %s, %s)")
        cursor.execute(self.sql, (food, id))
        db.commit()

    def joinTables(self, entry_date):
        self.sql = (
            " SELECT food.name, food.protein, food.carbohydrates, food.fat, food.calories FROM log_date JOIN food_date ON food_date.log_date_id= log_date.id JOIN food ON food.id=food_date.food_id WHERE log_date.entry_date= %s")
        cursor.execute(self.sql, (entry_date,))
        result = cursor.fetchall()
        return result


class AddDate:
    def addDate(self, s):
        input_date = datetime.strptime(s, '%Y-%m-%d')
        formatted_date = datetime.strftime(input_date, '%Y%m%d')
        self.sql = ("INSERT INTO log_date (entry_date) VALUES (%s)")
        cursor.execute(self.sql, (formatted_date,))
        db.commit()

    def getDate(self):
        self.sql = ("SELECT entry_date FROM log_date ORDER BY entry_date DESC")
        cursor.execute(self.sql)
        result = cursor.fetchall()

        dateList = []
        for i in result:
            d = {}
            d['single_date'] = i['entry_date']
            get_date = datetime.strptime(str(i['entry_date']), '%Y%m%d')
            d['date'] = datetime.strftime(get_date, '%B %d, %Y')
            dateList.append(d)

        return dateList

    def getParticularDate(self, d):
        self.sql = (" SELECT id,entry_date FROM log_date WHERE entry_date = %s")
        cursor.execute(self.sql, (d,))
        result = cursor.fetchone()
        date = datetime.strptime(str(result['entry_date']), '%Y%m%d')
        pretty_date = datetime.strftime(date, '%B %d, %Y')
        return [result['id'], pretty_date]


add = Add_food()
date = AddDate()
# print(add.getFood())
# print(add.getFoodItem())
# print(date.getDate())
# print(date.getParticularDate('20210704'))
food = add.getFood()

# for f in food:
#     print(f['name'])
# for name in add.getFoodItem():
#     print(name['name'])
# create_database()
# create_tables()
