import flask
from flask import jsonify, request, flash, request, redirect, url_for, render_template
import requests

fake_store_api_url = 'https://fakestoreapi.com/'

app = flask.Flask(__name__)
app.secret_key = '!@#$&^(*(*()&**%$%#@#'

# 1
"""1) Функция которая будет выводить все товары, она должна начинаться со слова get.... 
Можешь вывести все данные что есть у каждого товара или только названия, не важно"""


@app.route('/products', methods=['GET'])
def get_store_info():
    fake_store_products = 'https://fakestoreapi.com/products'
    try:
        response = requests.get(fake_store_products)
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to fetch data from Fake Store API: {str(e)}'})


# 2
"""2) Функция для добавление нового товара, она должна начинаться со слов create.... или add.... 
Тут нужно сделать функцию которая принимает такие параметры:
Заголовок title
Цена price
Описание description
Картинка - любая image
Категория category
В ответ должно прийти что товар добавлен и его ИД
В случае неудачи - сообщение об ошибке"""


'''@app.route('/add_post', methods=['POST', 'GET'])
def add_post():
    url = 'https://fakestoreapi.com/products'

    data = {
        'title': request.form.get('title'),
        'price': request.form.get('price'),
        'description': request.form.get('description'),
        'image': request.form.get('image'),
        'category': request.form.get('category')
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            flash('Item added to store')
            return jsonify({'added_product': response.json(), 'id_of_product': response.json()['id']}), 200
        else:
            flash('Failed to sent item to store')
            return jsonify({'error': 'Failed to sent item to store'}, response.status_code)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Request to Fake Store API failed: {str(e)}'}), 500

    return render_template('add_item.html')
'''
@app.route('/add_post', methods=['POST', 'GET'])
def add_post():
    if request.method == 'POST':
        url = 'https://fakestoreapi.com/products'

        data = {
            'title': request.form.get('title'),
            'price': request.form.get('price'),
            'description': request.form.get('description'),
            'image': request.form.get('image'),
            'category': request.form.get('category')
        }
        try:
            response = requests.post(url, json=data)
            if response.status_code == 201:
                flash('Item added to store')
                added_product = response.json()
                return render_template('add_item.html', added_product=added_product)
            else:
                flash('Failed to send item to store')
                error_message = f'Failed to send item to store. Status code: {response.status_code}'
                return render_template('add_item.html', error=error_message)
        except requests.exceptions.RequestException as e:
            error_message = f'Request to Fake Store API failed: {str(e)}'
            return render_template('add_item.html', error=error_message)

    return render_template('add_item.html')


# 3
"""3) Добавить функию для обновления информации о товаре, начинается со слов update...
Тут также как в функции с добавлением товара, но все поля не обязательные, т.е можно обновить только 1 поле, а таже обязательное поле ид
При успешном обновлении товара - вывести все данные"""


@app.route('/update_product/<int:product_id>', methods=['PATCH', 'PUT', 'GET'])
def update_product(product_id):
    url = f"https://fakestoreapi.com/products/{product_id}"

    data = {
        'title': request.form.get('title'),
        'price': request.form.get('price'),
        'description': request.form.get('description'),
        'image': request.form.get('image'),
        'category': request.form.get('category')
    }

    try:
        response = requests.patch(url, json=data)
        if response.status_code == 200:
            updated_product_id = response.json().get('id')
            flash(f'Item {product_id} updated')
            return jsonify({'updated_product': response.json(), 'updated_product_id': updated_product_id,
                            'message': f'Item {updated_product_id} updated successfully'}), 200

        else:
            flash('Failed to update item')
            return jsonify({'error': 'Failed to update item'}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Request to Fake Store API failed: {str(e)}'}), 500


# 4
"""4) Удаление товара, функция начинается на delete...
Функция должна принимать ид товара который нужно удалить"""
@app.route('/del_product/<int:id>', methods=['DELETE','GET'])
def delete_product(id):
    url = f"https://fakestoreapi.com/products/{id}"
    try:
        response = requests.delete(url)
        if response.status_code==200:
            flash(f"product {id} deleted")
            return jsonify({'deleted_product':id}),200
        else:
            flash(f"failed to delete product{id}")
            return jsonify({'error': f'failed to delete product{id}'}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Request to Fake Store API failed: {str(e)}'}), 500



if __name__ == '__main__':
    app.run(debug=True)
