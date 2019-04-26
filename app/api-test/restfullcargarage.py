# restfullbooker.py
import requests
from car_generator import GenerateCar

def _url(path):
    return 'http://10.100.195.200' + path

def get_cars(title="", brand="", price="", age=""):
    payload = {}
    if title:
        payload['title'] = title
    if brand:
        payload['brand'] = brand
    if price:
        payload['price'] = price
    if age:
        payload['age'] = age

    if payload:
        return requests.get(_url('/api/cars'), params=payload)
    else:
        return requests.get(_url('/api/cars'))

def describe_car(car_id):
    return requests.get(_url('/api/cars/{}'.format(car_id)))

def add_random_car():
    return add_car(GenerateCar())

def add_car(car):
    return requests.post(_url('/api/cars'), json=car)

def remove_car(car_id):
    return requests.delete(_url('/api/cars/{}'.format(car_id)))

def update_car(car_id, title = 'Jim', brand = 'Brown', price = 111, age = 8, services = {}):
    return requests.put(_url('/api/cars/{}'.format(car_id)), json={
        "title" : title,
        "brand" : brand,
        "price" : price,
        "age" : age,
        "services" : services
    })

