import flask
from flask import jsonify, request, flash, redirect, url_for, render_template
import requests

fake_store_api_url = 'https://fakestoreapi.com/'

app = flask.Flask(__name__)
app.secret_key = '!@#$&^(*(*()&**%$%#@#'

# Функция для получения информации о товаре по его ID
def get_product_info(product_id):
    fake_store_product_url = f"https://fakestoreapi.com/products/{product_id}"
    try:
        response = requests.get(fake_store_product_url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None

@app.route('/product/<int:product_id>', methods=['GET', 'DELETE'])
def display_product(product_id):
    product = get_product_info(product_id)
    return render_template('product.html', product=product)

# Функция для вывода всех товаров
@app.route('/', methods=['GET'])
@app.route('/products', methods=['GET'])
def get_all_products():
    fake_store_products_url = 'https://fakestoreapi.com/products'
    try:
        response = requests.get(fake_store_products_url)
        if response.status_code == 200:
            data = response.json()
            return render_template('products.html', products=data)
        else:
            return jsonify({'error': f'Failed to fetch data from Fake Store API: {response.status_code}'})
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to fetch data from Fake Store API: {str(e)}'})


# Функция для добавления нового товара
# Функция для добавления нового товара
@app.route('/add_product', methods=['POST','GET'])
def add_product():
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
                return redirect(url_for('get_all_products'))
            else:
                flash('Failed to send item to store')
                return redirect(url_for('get_all_products'))
        except requests.exceptions.RequestException as e:
            flash(f'Request to Fake Store API failed: {str(e)}')
            return redirect(url_for('get_all_products'))
    else:
        return render_template('add_item.html')

# Функция для обновления информации о товаре
@app.route('/update_product/<int:product_id>', methods=['POST', 'GET'])
def update_product(product_id):
    if request.method == 'POST':
        url = f"https://fakestoreapi.com/products/{product_id}"
        data = {
            'title': request.form.get('title'),
            'price': request.form.get('price'),
            'description': request.form.get('description'),
            'image': request.form.get('image'),
            'category': request.form.get('category')
        }
        try:
            response = requests.put(url, json=data)
            if response.status_code == 200:
                flash('Product updated successfully')
                return redirect(url_for('get_all_products'))
            else:
                flash('Failed to update product')
                return redirect(url_for('get_all_products'))
        except requests.exceptions.RequestException as e:
            flash(f'Request to Fake Store API failed: {str(e)}')
            return redirect(url_for('get_all_products'))

    elif request.method == 'GET':
        product_info = get_product_info(product_id)
        if product_info:
            return render_template('edit_product.html', product=product_info)
        else:
            flash('Product not found')
            return redirect(url_for('get_all_products'))


# Функция для удаления товара
@app.route('/del_product/<int:product_id>', methods=['POST', 'GET'])
def delete_product(product_id):
    if request.method == 'POST':
        url = f"https://fakestoreapi.com/products/{product_id}"
        try:
            response = requests.delete(url)
            if response.status_code == 200:
                flash(f"Product {product_id} deleted")
                return redirect(url_for('get_all_products'))
            else:
                flash(f"Failed to delete product {product_id}")
                return redirect(url_for('get_all_products'))
        except requests.exceptions.RequestException as e:
            flash(f"Request to Fake Store API failed: {str(e)}")
            return redirect(url_for('get_all_products'))
    else:
        # Обработка GET запроса
        return redirect(url_for('get_all_products'))


if __name__ == '__main__':
    app.run(debug=True)
