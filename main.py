from flask import Flask, request
from db import get_products, create_product

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    # return 'Hello World!'

    # return '<h1>Hello World!</h1>'

    # return html with css
    # return "<h1 style='color:red'>Hello World!</h1><p>This is a paragraph</p><p>This is another paragraph</p>"

    # render Jsom
    #some additional staff
    return {
        'name': 'john',
        'age': 21,
        'city': 'New York'
    }


@app.route('/products', methods=['GET', 'POST'])
def products_api():
    if request.method == 'GET':

        # get records from db
        products_records = get_products()

        products = []
        for product in products_records:
            products.append({'id': product[0], 'name': product[1], 'price': product[2]})

        return products

    if request.method == 'POST':
        request_json = request.get_json()

        name = request_json['name']
        price = request_json['price']

        id = create_product(name, price)

        return {
            'id': id,
            'name': name,
            'price': price
        }, 201

@app.route('/products/<int:product_id>', methods=['GET','DELETE'])
def product_api(product_id):
    if request.method == 'PUT':
        request_json = request.get_json()

        name = request_json['name']
        price = request_json['price']



if __name__ == '__main__':
    app.run(port=5000, debug=True)
