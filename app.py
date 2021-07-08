from flask import Flask, render_template, request
from sql import Add_food, AddDate
app = Flask(__name__)
add_food = Add_food()
add_date = AddDate()


def total():
    result = add_date.getDate()
    total_list = []
    for i in result:
        viewFood = add_food.joinTables(i['single_date'])
        # total = {}
        i['protein'] = 0
        i['carbohydrates'] = 0
        i['fat'] = 0
        i['calories'] = 0
        for food in viewFood:
            i['protein'] += int(food['protein'])
            i['carbohydrates'] += int(food['carbohydrates'])
            i['fat'] += int(food['fat'])
            i['calories'] += int(food['calories'])
        total_list.append(i)
    return total_list


# print(total())


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        add_date.addDate(request.form['date'])

    result = add_date.getDate()
    total_list = total()

    return render_template('home.html', results=result, total=total_list)


@app.route('/view/<date>', methods=['GET', 'POST'])
def view(date):
    result = add_date.getParticularDate(date)
    if request.method == 'POST':
        param = request.form['food-select']
        id = result[0]
        add_food.addFoodToDate(param, id)

    food_items = add_food.getFoodItem()
    viewFood = add_food.joinTables(date)

    total = {}
    total['protein'] = 0
    total['carbohydrates'] = 0
    total['fat'] = 0
    total['calories'] = 0
    for food in viewFood:
        total['protein'] += food['protein']
        total['carbohydrates'] += food['carbohydrates']
        total['fat'] += food['fat']
        total['calories'] += food['calories']

    return render_template('day.html', result=result, food_items=food_items, viewfood=viewFood, date=date,
                           total=total)


@app.route("/food", methods=['GET', 'POST'])
def food():
    if request.method == 'POST':
        name = request.form['food-name']
        protein = int(request.form['protein'])
        carbohydrates = int(request.form['carbohydrates'])
        fats = int(request.form['fat'])
        calories = protein*4+carbohydrates*4+fats*4
        add_food.addFood(name, protein, carbohydrates, fats, calories)
    result = add_food.getFood()
    return render_template('add_item.html', results=result)


if __name__ == '__main__':
    app.run(debug=True)
