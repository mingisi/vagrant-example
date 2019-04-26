# test_restfull_cars.py
import restfullcargarage
from assertpy import assert_that


def test_addcar():
    resp = restfullcargarage.add_random_car()
    assert_that(resp.ok, 'HTTP Request OK').is_true()

def test_get_cars_by_id():
    #TODO: load test data to db and then run this test insted of adding via api
    new_car = restfullcargarage.add_random_car().json()
    resp = restfullcargarage.describe_car(new_car['_id'])
    assert_that(resp.ok, 'HTTP Request OK').is_true()
    assert_that(resp.json()['title'], 'Title').contains(new_car['title'])

def test_updatecar():
    new_car = restfullcargarage.add_random_car().json()['_id']
    resp = restfullcargarage.update_car(new_car)
    resp2 = restfullcargarage.describe_car(new_car)
    assert_that(resp.ok, 'HTTP Request OK').is_true()
    assert_that(resp2.json()["title"], 'Title').contains('Jim')

def test_removecar():
    new_car = restfullcargarage.add_random_car().json()['_id']
    resp = restfullcargarage.remove_car(new_car)
    assert_that(resp.ok, 'HTTP Request OK').is_true()