import flask
from flask import jsonify, request, flash
import requests

fake_store_api_url = 'https://fakestoreapi.com/'


app = flask.Flask(__name__)

#1
"""1) Функция которая будет выводить все товары, она должна начинаться со слова get.... 
Можешь вывести все данные что есть у каждого товара или только названия, не важно"""

@app.route('/products', methods=['GET'])
def get_store_info():
    fake_store_products = 'https://fakestoreapi.com/products'
    response = requests.get(fake_store_products)
    try:
        data = response.json()

        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to fetch data from Fake Store API: {str(e)}'})


#2
"""2) Функция для добавление нового товара, она должна начинаться со слов create.... или add.... 
Тут нужно сделать функцию которая принимает такие параметры:
Заголовок title
Цена price
Описание description
Картинка - любая image
Категория category
В ответ должно прийти что товар добавлен и его ИД
В случае неудачи - сообщение об ошибке"""
@app.route('/add_post', methods= ['POST','GET'])
def add_post():
    url = 'https://fakestoreapi.com/products'
    data = {
        'title':'smth',
        'price':20,
        'description':'new item',
        'image':'https:url',
        'category':'item'
    }
    response = requests.post(url, json=data)
    if requests.methods == "POST":

        if response.status_code == 200:
            flash('item added to store')
            print(response.json())

        else:
            flash('item not added to store')
            print(response.status_code)





    return 

#3
"""3) Добавить функию для обновления информации о товаре, начинается со слов update...
Тут также как в функции с добавлением товара, но все поля не обязательные, т.е можно обновить только 1 поле, а таже обязательное поле ид
При успешном обновлении товара - вывести все данные"""




#4
"""4) Удаление товара, функция начинается на delete...
Функция должна принимать ид товара который нужно удалить"""


if __name__ == '__main__':
    app.run(debug=True)