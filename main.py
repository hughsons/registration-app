"""

Imagine we want to build a /api/user-cart-summary/<user_id> endpoint for our app.
It should collect the following data from FakeStoreAPI:
User details → /users/{id}
User cart details → /carts/{id}
For each product in the cart, product information → /products/{productId}
Then combine everything and return one unified JSON response.”
API Details
curl --location 'https://fakestoreapi.com/users/1'
{
  "address": {
    "geolocation": {
      "lat": "-37.3159",
      "long": "81.1496"
    },
    "city": "kilcoole",
    "street": "new road",
    "number": 7682,
    "zipcode": "12926-3874"
  },
  "id": 1,
  "email": "john@gmail.com",
  "username": "johnd",
  "password": "m38rmF$",
  "name": {
    "firstname": "john",
    "lastname": "doe"
  },
  "phone": "1-570-236-7033",
  "__v": 0
}
curl --location 'https://fakestoreapi.com/carts/1'
{
  "id": 1,
  "userId": 1,
  "date": "2020-03-02T00:00:00.000Z",
  "products": [
    {
      "productId": 1,
      "quantity": 4
    },
    {
      "productId": 2,
      "quantity": 1
    },
    {
      "productId": 3,
      "quantity": 6
    }
  ],
  "__v": 0
}
curl --location 'https://fakestoreapi.com/products/1'
{
  "id": 1,
  "title": "Fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops",
  "price": 109.95,
  "description": "Your perfect pack for everyday use and walks in the forest. Stash your laptop (up to 15 inches) in the padded sleeve, your everyday",
  "category": "men's clothing",
  "image": "<https://fakestoreapi.com/img/81fPKd-2AYL._AC_SL1500_t.png>",
  "rating": {
    "rate": 3.9,
    "count": 120
  }
}

"""

from django.http import JsonResponse
import requests

BASE_URL = 'https://fakestoreapi.com'


def user_cart_summary(request, user_id):

    try:
        user = request.get(f"{BASE_URL}/users/{user_id}").json()
        cart = request.get(f"{BASE_URL}/cart/{user_id}").json()

        product_items=[]

        for item in cart.get("products",[]):
            product_id = item["productId"]
            qty = item["quantity"]

            p = requests.get(f"{BASE_URL}/products/{product_id}")

            product_items.append({
                "product_id":product_id,
                "title":p.get("title"),
                "price":p.get("price"),
                "quantity":qty

            })

            response = {
                "user": user,
                "cart_id":cart.get("id"),
                "date":cart.get("date"),
                "items":product_items,

            }
            return Jsonresponse(response)
    except Exceptiopn as e:
        return JsonResponse({e})



def call_with_retry(  )
    retries = [0.2, 0.5, 10]

    for wait in retries:
        try:
            response = request()
            return response
        except:
            sleep(wait)





















                            )
