from zeep import Client

client = Client(
    wsdl='http://serve-soaps-15aqnx3smguqk-1222517465.ap-southeast-1.elb.amazonaws.com/?wsdl')
#client = Client(
#    wsdl='http://127.0.0.1:8000/?wsdl')

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
