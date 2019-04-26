#booking_generator.py
from random import choice

def GenerateCar():
    title = choice(['Seat', 'Bristol', 'Daihatsu', 'Jaguar', 'TVR', 'Porsche'])
    brand = choice(['Smart', 'Dodge', 'Mini', 'Jaguar'])
    price = choice([111,112,113,114,115,116,200,999])
    age = choice([True, False])
    service_name = choice(['Seat Alirus','Daihatsu Aslands','Jaguar Aprus','Porsche Andnildives','TVR Borab'])
    service_date = choice(['2018-02-5','2018-03-05','2018-04-05','2018-05-05','2018-06-20'])
    
    output = {
        "title": title,
        "brand": brand,
        "price": price,
        "age" : age,
        "services" : {
            service_name : service_date
        }
    }

    return(output)