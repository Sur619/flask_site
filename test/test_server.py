import requests  # пайтон пакет который позволяет отпралять запросы.


def test_product_create():
    # create product
    response = requests.post('http://localhost:5000/products', json={
        'name': 'Fanta',
        'price': 43
    })

    print(response.status_code)
    print(response.json())


def test_product_update() -> object:
    # update product
    response = requests.put('http://localhost:5000/products/1', json={
        'name': 'Sprite',
        'price': 100
    })


if __name__ == '__main__':
    test_product_update()
