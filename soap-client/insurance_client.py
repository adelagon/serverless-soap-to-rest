from zeep import Client

client = Client(
    wsdl='http://localhost:8000/?wsdl')

client.wsdl.dump()
print(
    client.service.submit_car_application(
        first_name="Juan",
        last_name="Dela Cruz",
        make="Mitsubishi",
        model="Lancer EX",
        year=2013,
        current_price=400000
    )
)
